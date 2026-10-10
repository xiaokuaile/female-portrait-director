[English](README.md) | [简体中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)

# Female Portrait Prompt Director Skill

Turn a few portrait inputs into a coherent, camera-ready prompt. With a suitable image tool connected to the host, the Skill can also direct image generation or edits from authorized references.

[![skills.sh](https://skills.sh/b/liyue-aigc/female-portrait-director)](https://skills.sh/liyue-aigc/female-portrait-director)
[![GitHub stars](https://img.shields.io/github/stars/liyue-aigc/female-portrait-director?style=flat)](https://github.com/liyue-aigc/female-portrait-director/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This is not a generic prompt collection. It locks explicit requirements, chooses one visual route, and directs the subject, action, clothing, scene, camera, lighting, and finish as one photographable moment. Subjects are fictional, clearly adult women unless an authorized adult reference is provided.

## See the difference

| Clean lifestyle | Urban fashion | Gufeng xianxia |
| --- | --- | --- |
| ![Sunlit clean lifestyle portrait by a cafe window](assets/cases/01-clean-lifestyle.png) | ![Urban fashion street portrait outside a shopping mall](assets/cases/02-urban-fashion.png) | ![Red-and-gold gufeng xianxia portrait](assets/cases/03-gufeng-xianxia.png) |
| Hong Kong street | French effortless | Pure-desire curves |
| ![Golden-hour Hong Kong street portrait](assets/cases/04-retro-hongkong-street.png) | ![French effortless portrait on a Paris balcony](assets/cases/05-french-lazy.png) | ![Pure-desire curve-focused lifestyle portrait](assets/cases/06-pure-desire-curve.png) |

The six cases cover clean lifestyle, urban fashion, gufeng xianxia, Hong Kong street photography, French effortless portraiture, and curve-focused lifestyle direction.

## Try it in 60 seconds

Install with the open-source `skills` CLI:

```bash
npx skills@1.7.2 add https://github.com/xiaokuaile/female-portrait-director/tree/main/skills/female-portrait-director --skill female-portrait-director --agent codex --copy -g
```

Start a new agent session, then paste:

```text
Use $female-portrait-director to generate an image directly:
Style: clean lifestyle portrait
Scene: quiet cafe window seat in the afternoon
Outfit: ivory knitted cardigan + light inner top
Mood: gentle, natural, clearly adult
Aspect ratio: 3:4
```

For a copy-ready prompt instead of an image, remove “generate an image directly.” The Skill returns locked parameters, a directed prompt, and negative constraints.

## Agent compatibility

The upstream release reports installation verification of its complete distribution package with the `skills` CLI for the following targets:

| Agent | Install package | Prompt workflow | Direct image workflow |
| --- | --- | --- | --- |
| Codex | Upstream verified | Upstream runtime verified | Depends on the available image tool and its edit support |
| Claude Code | Upstream verified | Agent Skills compatible | Depends on the connected image tool |
| Cursor | Upstream verified | Agent Skills compatible | Depends on the connected image tool |
| GitHub Copilot | Upstream verified | Agent Skills compatible | Depends on the connected image tool |
| Gemini CLI | Upstream verified | Agent Skills compatible | Depends on the connected image tool |

“Installer-verified” means the CLI copied `SKILL.md` and its referenced modules into the target package. The runtime claim above belongs to the upstream release environment; it does not establish installation, tool availability, or image-edit fidelity on another device. This repository contains Markdown instructions, not an image model or editing engine. Prompt generation, successful image-tool execution, and image fidelity are separate acceptance levels; see the [validation procedure](docs/reference-fidelity-validation.md).

## Supported Styles

- Clean lifestyle portraits
- Restrained curve-focused lifestyle portraits
- Urban fashion photography
- Gufeng fantasy portraits
- E-commerce clothing model images
- Retro Hong Kong portraits
- French relaxed portraits
- New Chinese oriental portraits
- Sporty active portraits
- Travel vacation portraits
- Studio-retouched portraits
- Oriental voluptuous portraits
- Cold xianxia enhanced portraits
- Bright luxury gufeng portraits
- Ultra-close realistic face portraits
- Ancient noblewoman dewy-makeup portraits
- Black-pearl dark-gold CCD curve portraits
- Energetic voluptuous soft-CCD lifestyle portraits
- Cold-white clear CCD curve portraits
- Low-key cinematic photography

See the [first-use guide](skill/help.md) for the 20-style menu, input templates, route-plus-overlay combination rules, and a complete parameter-to-five-paragraph-prompt example.

## Core Capabilities

- Lock user-specified parameters and only refine or stabilize them.
- Route each request through one on-demand style file and avoid conflicting style keywords.
- Parse face, body, outfit, scene, camera and pose, lighting, and filter modules.
- Expand short parameters into a coherent photographed moment instead of mechanically repeating them.
- Fuse the expanded modules into natural, detailed, copy-ready prompts with photography-director intent.
- Preserve clothing-display priority for e-commerce images and explicit safety boundaries for curve-focused portraits.
- Direct authorized reference-image workflows with explicit preservation rules.

## Photo fidelity and output capability

This fork retains Li Yue’s original work and adds stricter photo-preservation defaults. For photo style conversion, the default `source_faithful_stylization` mode locks the original identity, facial features, hairstyle, clothing, pose and actions, subject count, camera angle, composition, and crop. Only requested changes such as color, lighting appearance, or rendering style are allowed; a style route cannot silently replace the person, outfit, or framing.

Optional `reference mode` / `参考图模式` values are `source_faithful_stylization`, `identity_restage` (change only expressly allowed items), and `protected_region_edit`. Existing parameters continue to work. Supply allowed changes, protected regions, and original image dimensions when needed; missing optional fields do not unlock protected features. A request for prompts only remains a prompt request even with uploaded images.

If “keep the original unchanged” requires exact original pixels, `protected_region_edit` must use deterministic region protection, such as preserving and compositing the source pixels outside an edit mask, followed by a pixel-equality check in the protected region. Generative instructions alone cannot promise that result. If the connected tool cannot provide that workflow, report the limitation before generation and provide the requested prompt or editing plan. See [reference-image rules](skill/core/reference-image-lock.md).

## Installation details

The verified CLI version `skills@1.7.2` requires [Node.js](https://nodejs.org/) `>=22.20.0`. The commands here install this fork; the [original upstream repository](https://github.com/liyue-aigc/female-portrait-director) remains the author’s project. Before updating an existing installation, back up local changes and confirm its recorded source points to the intended fork and revision. A generic update of an upstream installation will not adopt this fork’s rules. For a CLI-managed global installation of this exact Skill, the supported command is:

```bash
npx skills@1.7.2 update female-portrait-director -g
```

In `skills@1.7.2`, the name filters to this Skill and `-g` selects global scope; use `-p` instead for the current project. Omitting the name can update every tracked Skill in the selected scope. Update follows the recorded source and performs reinstalls, potentially replacing local edits; removing `-y` does not make it a preview or require confirmation before every replacement. The update command has no `--agent` filter. Check the source and back up first. See the [official CLI update documentation](https://github.com/vercel-labs/skills/blob/671e8c320810d36fed80fac5f1a2c1bf7e82d812/README.md#skills-update).

### Manual Codex install with Git

Alternatively, clone the complete repository into a new Codex skill directory. Keep its root `SKILL.md`, `skill/`, `docs/`, and `agents/` together. The CLI instead installs the self-contained `skills/female-portrait-director/` distribution. Do not copy `SKILL.md` alone or overwrite an existing directory containing local configuration; review and merge an existing installation. See the [installation checks](docs/reference-fidelity-validation.md).

Windows PowerShell:

```powershell
git clone https://github.com/xiaokuaile/female-portrait-director.git "$env:USERPROFILE\.codex\skills\female-portrait-director"
```

macOS or Linux:

```bash
git clone https://github.com/xiaokuaile/female-portrait-director.git "${CODEX_HOME:-$HOME/.codex}/skills/female-portrait-director"
```

Restart Codex or start a new conversation, then invoke:

```text
$female-portrait-director
```

The first parameter-free invocation displays the V1.6 tutorial: all 20 implemented styles, basic and advanced templates, style-plus-mood combination guidance, a detailed prompt example, and direct-image or authorized-reference workflows.

## Example: Parameters to Directed Prompt

The Skill does more than restate the input. It preserves requested parameters, fills in missing visual details, and produces locked parameters, module analysis, a final prompt, and negative constraints.

```text
Portrait style: Gufeng xianxia beauty portrait
Scene: Traditional courtyard corridor surrounded by misty mountains and water
Outfit: Moon-white Tang-inspired fantasy wide-sleeve robe + flowing pibo scarf + silver embroidered waist sash
Mood: Cool, distant, ethereal
Facial direction: Classical East Asian beauty
Body direction: Slender and delicate figure
Camera direction: Slight side-facing standing pose, half-body to thigh framing
Lighting: Cool soft light
Filter: Cool ethereal gufeng filter
Aspect ratio: 9:16
Platform use: Character portrait
```

![Gufeng xianxia prompt expansion example](assets/examples/gufeng-director-output.jpg)

## Output Format

```text
1. Locked parameters
2. Module analysis
3. Final prompt
4. Negative constraints
```

## Repository Structure

```text
.
├── README.md
├── README_zh.md
├── README_ja.md
├── README_ko.md
├── SKILL.md
├── agents/openai.yaml
├── assets/examples/
├── skill/
│   ├── skill.md
│   ├── style-registry.md
│   ├── help.md
│   ├── public_instructions.md
│   ├── parameter_schema.md
│   ├── usage_examples.md
│   ├── core/
│   ├── references/
│   │   ├── director-expansion.md
│   │   └── visual-libraries.md
│   └── routes/
│       ├── beauty/
│       ├── commercial/
│       ├── curve/
│       ├── fantasy/
│       ├── fashion/
│       ├── lifestyle/
│       ├── oriental/
│       └── realism/
├── docs/
│   ├── style_guide.md
│   ├── prompt_safety.md
│   ├── versioning.md
│   └── faq.md
└── examples/
```

## Safety Boundaries

Text-only generation defaults to fictional, clearly adult subjects. Reference-image workflows may preserve the identity of the user or an authorized adult subject, and may preserve product visuals that the user has the right to use. The project must not be used for sexualized minors, explicit nudity, non-consensual images, deceptive identity content, harassment, defamation, privacy violations, or other unlawful purposes. See [prompt_safety.md](docs/prompt_safety.md) and [DISCLAIMER.md](DISCLAIMER.md) for details.

## License

This project is licensed under the [MIT License](LICENSE). The MIT License permits use, copying, modification, merging, publishing, distribution, sublicensing, and selling copies. The safety boundaries are responsible-use guidelines and do not alter the standard MIT License terms.

## Author and Version

- Author: Li Yue (李岳)
- Version: `FEMALE-PORTRAIT-DIRECTOR-V1.6`
- Project: `Female Portrait Prompt Director Skill`
