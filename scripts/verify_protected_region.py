#!/usr/bin/env python3
"""Read-only decoded-pixel check; requires Pillow, never edits input files.

Mask coordinates refer to the original image: 0 protects, 255 allows editing.
Offset locates the original top-left corner in the result (e.g. outpainting).
Supported modes are L, LA, RGB, RGBA, and CMYK; no color/alpha conversion.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def verify(original_path, result_path, offset=(0, 0), mask_path=None):
    with Image.open(original_path) as original, Image.open(result_path) as result:
        original.load()
        result.load()
        if getattr(original, "n_frames", 1) != 1 or getattr(result, "n_frames", 1) != 1:
            raise ValueError("Only single-frame images are supported.")
        supported = {"L", "LA", "RGB", "RGBA", "CMYK"}
        if original.mode not in supported or result.mode != original.mode:
            raise ValueError("Modes must match and be L, LA, RGB, RGBA or CMYK; no conversion is performed.")
        if original.info.get("icc_profile") != result.info.get("icc_profile"):
            raise ValueError("ICC profiles differ; pixel equality would not prove the same color interpretation.")
        orientation = original.getexif().get(274, 1)
        if orientation != result.getexif().get(274, 1):
            raise ValueError("EXIF orientations differ; use consistently oriented files and coordinates.")
        x, y = offset
        width, height = original.size
        if x < 0 or y < 0 or x + width > result.width or y + height > result.height:
            raise ValueError("The full original rectangle must fit inside the result at the specified offset.")
        allowed = bytes(width * height)
        if mask_path is not None:
            with Image.open(mask_path) as mask:
                mask.load()
                if getattr(mask, "n_frames", 1) != 1 or mask.mode != "L" or mask.size != original.size:
                    raise ValueError("Mask must be a single-frame L image with the original dimensions.")
                allowed = mask.tobytes()
                if any(value not in (0, 255) for value in allowed):
                    raise ValueError("Mask must be binary: black (0) protects, white (255) allows edits.")
        protected = allowed.count(0)
        if protected == 0:
            raise ValueError("No protected pixels; this cannot validate a preservation claim.")
        original_bytes = original.tobytes()
        region = result.crop((x, y, x + width, y + height))
        result_bytes = region.tobytes()
        bands = len(original.getbands())
        differences = 0
        first_difference = None
        for pixel_index, permission in enumerate(allowed):
            if permission == 255:
                continue
            start = pixel_index * bands
            if original_bytes[start:start + bands] != result_bytes[start:start + bands]:
                differences += 1
                if first_difference is None:
                    source_x = pixel_index % width
                    source_y = pixel_index // width
                    first_difference = {
                        "original": [source_x, source_y],
                        "result": [source_x + x, source_y + y],
                    }
        return {
            "passed": differences == 0,
            "original_size": list(original.size),
            "result_size": list(result.size),
            "offset": [x, y],
            "mode": original.mode,
            "exif_orientation": orientation,
            "protected_pixels": protected,
            "different_pixels": differences,
            "first_difference": first_difference,
            "scope": "Decoded protected pixels only; not identity recognition or whole-file byte equality.",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("result", type=Path)
    parser.add_argument("--offset", nargs=2, type=int, default=(0, 0), metavar=("X", "Y"))
    parser.add_argument("--mask", type=Path, help="Original-size binary L mask: black protects, white permits editing")
    args = parser.parse_args()
    try:
        report = verify(args.original, args.result, args.offset, args.mask)
    except (OSError, ValueError) as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
