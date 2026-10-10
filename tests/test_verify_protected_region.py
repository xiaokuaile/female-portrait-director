"""Regression tests with tiny synthetic inputs; no image generation is used."""

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_protected_region.py"
SPEC = importlib.util.spec_from_file_location("verify_protected_region", SCRIPT)
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class ProtectedRegionVerificationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="protected-region-tests-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def image(self, name, mode="RGB", size=(3, 2), color=None, changes=(), **metadata):
        if color is None:
            color = {
                "L": 37,
                "LA": (37, 190),
                "RGB": (37, 61, 109),
                "RGBA": (37, 61, 109, 190),
                "CMYK": (12, 34, 56, 78),
            }.get(mode, 0)
        extension = ".tiff" if mode == "CMYK" else ".png"
        path = self.root / (name + extension)
        with Image.new(mode, size, color) as image:
            for coordinates, value in changes:
                image.putpixel(coordinates, value)
            image.save(path, **metadata)
        return path

    @contextmanager
    def unchanged_files(self, *paths):
        def snapshot(path):
            stat = path.stat()
            return hashlib.sha256(path.read_bytes()).hexdigest(), stat.st_size, stat.st_mtime_ns

        paths = [Path(path) for path in paths if path is not None and Path(path).exists()]
        before = {path: snapshot(path) for path in paths}
        try:
            yield
        finally:
            self.assertEqual(before, {path: snapshot(path) for path in paths})

    def verify(self, original, result, offset=(0, 0), mask=None):
        with self.unchanged_files(original, result, mask):
            return VERIFIER.verify(original, result, offset=offset, mask_path=mask)

    def cli(self, original, result, *arguments, mask=None):
        command = [sys.executable, str(SCRIPT), str(original), str(result), *arguments]
        if mask is not None:
            command.extend(["--mask", str(mask)])
        with self.unchanged_files(original, result, mask):
            completed = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(completed.stderr, "")
        return completed.returncode, json.loads(completed.stdout)

    def test_equal_rgb_rgba_and_other_supported_modes(self):
        for mode in ("RGB", "RGBA", "L", "LA", "CMYK"):
            with self.subTest(mode=mode):
                original = self.image("equal-original-" + mode, mode=mode)
                result = self.image("equal-result-" + mode, mode=mode)
                report = self.verify(original, result)
                self.assertTrue(report["passed"])
                self.assertEqual(report["mode"], mode)
                self.assertEqual(report["protected_pixels"], 6)
                self.assertEqual(report["different_pixels"], 0)
                self.assertIsNone(report["first_difference"])

    def test_one_protected_rgb_pixel_change_fails_and_reports_coordinates(self):
        original = self.image("pixel-original")
        result = self.image("pixel-result", changes=[((2, 1), (38, 61, 109))])
        report = self.verify(original, result)
        self.assertFalse(report["passed"])
        self.assertEqual(report["different_pixels"], 1)
        self.assertEqual(report["first_difference"], {"original": [2, 1], "result": [2, 1]})

    def test_alpha_only_change_in_a_protected_pixel_fails(self):
        original = self.image("alpha-original", mode="RGBA")
        result = self.image("alpha-result", mode="RGBA", changes=[((1, 0), (37, 61, 109, 191))])
        report = self.verify(original, result)
        self.assertFalse(report["passed"])
        self.assertEqual(report["different_pixels"], 1)
        self.assertEqual(report["first_difference"]["original"], [1, 0])

    def test_changes_inside_white_allowed_mask_area_pass(self):
        original = self.image("allowed-original", mode="RGBA")
        result = self.image("allowed-result", mode="RGBA", changes=[((2, 1), (255, 0, 0, 0))])
        mask = self.image("allowed-mask", mode="L", color=0, changes=[((2, 1), 255)])
        report = self.verify(original, result, mask=mask)
        self.assertTrue(report["passed"])
        self.assertEqual(report["protected_pixels"], 5)
        self.assertEqual(report["different_pixels"], 0)

    def test_black_mask_pixel_change_still_fails(self):
        original = self.image("masked-original")
        result = self.image("masked-result", changes=[((0, 0), (0, 0, 0))])
        mask = self.image("masked-mask", mode="L", color=0, changes=[((2, 1), 255)])
        report = self.verify(original, result, mask=mask)
        self.assertFalse(report["passed"])
        self.assertEqual(report["different_pixels"], 1)

    def test_offset_outpainting_passes_and_difference_coordinates_include_offset(self):
        original = self.image("offset-original")
        result = self.root / "offset-result.png"
        with Image.new("RGB", (6, 5), (255, 0, 0)) as expanded:
            with Image.open(original) as source:
                expanded.paste(source, (2, 1))
            expanded.save(result)
        report = self.verify(original, result, offset=(2, 1))
        self.assertTrue(report["passed"])
        self.assertEqual(report["original_size"], [3, 2])
        self.assertEqual(report["result_size"], [6, 5])
        self.assertEqual(report["offset"], [2, 1])
        with Image.open(result) as expanded:
            expanded.putpixel((4, 2), (0, 0, 0))
            expanded.save(result)
        report = self.verify(original, result, offset=(2, 1))
        self.assertFalse(report["passed"])
        self.assertEqual(report["first_difference"], {"original": [2, 1], "result": [4, 2]})

    def test_negative_or_out_of_bounds_offset_is_rejected(self):
        original = self.image("bounds-original")
        result = self.image("bounds-result", size=(4, 3))
        for offset in ((-1, 0), (0, -1), (2, 0), (0, 2)):
            with self.subTest(offset=offset):
                with self.assertRaisesRegex(ValueError, "full original rectangle"):
                    self.verify(original, result, offset=offset)
        too_small = self.image("bounds-too-small", size=(2, 2))
        with self.assertRaisesRegex(ValueError, "full original rectangle"):
            self.verify(original, too_small)

    def test_mode_mismatch_and_unsupported_modes_are_rejected(self):
        original = self.image("mode-original")
        rgba_result = self.image("mode-rgba-result", mode="RGBA")
        with self.assertRaisesRegex(ValueError, "Modes must match"):
            self.verify(original, rgba_result)
        palette_original = self.image("mode-palette-original", mode="P")
        palette_result = self.image("mode-palette-result", mode="P")
        with self.assertRaisesRegex(ValueError, "Modes must match"):
            self.verify(palette_original, palette_result)

    def test_icc_profile_mismatch_or_missing_profile_is_rejected(self):
        original = self.image("icc-original", icc_profile=b"test-profile-a")
        same = self.image("icc-same", icc_profile=b"test-profile-a")
        self.assertTrue(self.verify(original, same)["passed"])
        for name, metadata in (("different", {"icc_profile": b"test-profile-b"}), ("missing", {})):
            with self.subTest(profile=name):
                result = self.image("icc-" + name, **metadata)
                with self.assertRaisesRegex(ValueError, "ICC profiles differ"):
                    self.verify(original, result)

    def test_exif_orientation_mismatch_is_rejected_and_matching_orientation_passes(self):
        exif = Image.Exif()
        exif[274] = 6
        original = self.image("exif-original", exif=exif)
        same = self.image("exif-same", exif=exif)
        self.assertEqual(self.verify(original, same)["exif_orientation"], 6)
        result = self.image("exif-default")
        with self.assertRaisesRegex(ValueError, "EXIF orientations differ"):
            self.verify(original, result)

    def test_nonbinary_mask_is_rejected(self):
        original = self.image("nonbinary-original")
        result = self.image("nonbinary-result")
        mask = self.image("nonbinary-mask", mode="L", color=0, changes=[((1, 1), 128)])
        with self.assertRaisesRegex(ValueError, "Mask must be binary"):
            self.verify(original, result, mask=mask)

    def test_all_white_mask_is_rejected(self):
        original = self.image("white-original")
        result = self.image("white-result")
        mask = self.image("white-mask", mode="L", color=255)
        with self.assertRaisesRegex(ValueError, "No protected pixels"):
            self.verify(original, result, mask=mask)

    def test_mask_size_and_mode_are_rejected(self):
        original = self.image("invalid-mask-original")
        result = self.image("invalid-mask-result")
        masks = {
            "size": self.image("invalid-mask-size", mode="L", size=(2, 2), color=0),
            "mode": self.image("invalid-mask-rgb", mode="RGB", color=(0, 0, 0)),
        }
        for kind, mask in masks.items():
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(ValueError, "single-frame L image with the original dimensions"):
                    self.verify(original, result, mask=mask)

    def test_multiframe_image_is_rejected(self):
        original = self.image("animated-original")
        result = self.root / "animated-result.png"
        with Image.new("RGB", (3, 2), (37, 61, 109)) as first:
            with Image.new("RGB", (3, 2), (38, 61, 109)) as second:
                first.save(result, save_all=True, append_images=[second])
        with self.assertRaisesRegex(ValueError, "Only single-frame images"):
            self.verify(original, result)

    def test_cli_exit_zero_for_equality_one_for_difference_two_for_invalid_input(self):
        original = self.image("cli-original")
        equal = self.image("cli-equal")
        code, report = self.cli(original, equal)
        self.assertEqual(code, 0)
        self.assertTrue(report["passed"])

        changed = self.image("cli-changed", changes=[((0, 0), (0, 0, 0))])
        code, report = self.cli(original, changed)
        self.assertEqual(code, 1)
        self.assertFalse(report["passed"])
        self.assertEqual(report["different_pixels"], 1)

        mask = self.image("cli-invalid-mask", mode="L", color=255)
        code, report = self.cli(original, equal, mask=mask)
        self.assertEqual(code, 2)
        self.assertFalse(report["passed"])
        self.assertIn("No protected pixels", report["error"])

        code, report = self.cli(original, self.root / "missing.png")
        self.assertEqual(code, 2)
        self.assertFalse(report["passed"])
        self.assertIn("error", report)

    def test_cli_accepts_offset_and_mask_options(self):
        original = self.image("cli-options-original")
        result = self.root / "cli-options-result.png"
        with Image.new("RGB", (5, 4), (255, 255, 255)) as expanded:
            with Image.open(original) as source:
                expanded.paste(source, (1, 1))
            expanded.putpixel((3, 2), (0, 0, 0))
            expanded.save(result)
        mask = self.image("cli-options-mask", mode="L", color=0, changes=[((2, 1), 255)])
        code, report = self.cli(original, result, "--offset", "1", "1", mask=mask)
        self.assertEqual(code, 0)
        self.assertEqual(report["offset"], [1, 1])
        self.assertEqual(report["protected_pixels"], 5)


if __name__ == "__main__":
    unittest.main()
