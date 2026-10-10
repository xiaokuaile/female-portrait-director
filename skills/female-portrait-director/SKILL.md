---
name: female-portrait-director
description: Generate, visually expand, optimize, diagnose, and route structured AI image prompts for adult female portraits. Use for lifestyle, curve-focused, fashion, oriental, fantasy, realism, beauty, CCD, low-key cinematic, studio, sport, travel, and e-commerce portrait requests; onboarding or usage help; parameter recommendations; prompt rewrites; image-to-prompt preparation; direct image generation; or identity- and product-preserving edits from authorized reference images. Preserve explicit user parameters and locked reference subjects while creating a coherent photography-directed scene.
---

# Female Portrait Director

Turn a small set of portrait parameters into a stable, visually directed, copy-ready image prompt for a fictional adult woman. Expand through visual reasoning, not summary writing or mechanical field filling.

## Required loading order

1. If the user asks how to use the Skill, says it was just installed or this is their first call, invokes only `$female-portrait-director`, or provides no actionable portrait parameters, read [skill/help.md](skill/help.md) and return its concise onboarding tutorial. Do not load a Route for a help-only request.
2. Read [skill/skill.md](skill/skill.md) for the canonical workflow.
3. For uploaded-image tasks, before loading route defaults, filling missing parameters, or expanding the image, read [skill/core/reference-image-lock.md](skill/core/reference-image-lock.md). Establish image roles, preservation mode, protected features, and explicitly allowed changes. A request to stylize the uploaded photo defaults to `source_faithful_stylization`; use `identity_restage` only for explicitly requested restaging and `protected_region_edit` for an unchanged original region.
4. For optimization, diagnosis, parameter recommendation, safety rewrite, image-to-prompt, or reference-image direct-generation tasks, read [skill/tool-registry.md](skill/tool-registry.md) and only the selected file under `skill/tools/`.
5. Read [skill/style-registry.md](skill/style-registry.md). Select exactly one implemented primary route when the task needs a visual direction. Do not invent a placeholder extension route.
6. Read only the selected file under `skill/routes/`.
7. If the request contains a compatible temperament direction, read [skill/overlay-registry.md](skill/overlay-registry.md) and only the selected file under `skill/overlays/`.
8. Read [skill/core/director-gate.md](skill/core/director-gate.md). Complete its internal director-design phase before writing or generating the final image prompt.
9. Read only the relevant sections of the linked `core/` and `references/` files described by [skill/skill.md](skill/skill.md).

## Operating rules

- Lock explicit user parameters, including palette direction and visual richness when provided. Expand them without silently replacing them.
- Treat onboarding as a separate help mode. Show the V1.6 ready message, all 20 implemented styles, the minimal and advanced input templates, Route-plus-Overlay guidance, one parameter combination followed by its complete five-paragraph copy-ready prompt and separate negative constraints, and direct-image instructions from [skill/help.md](skill/help.md). Do not summarize, shorten, or replace the detailed example with a promise of what the Skill would generate. If the same request already contains actionable portrait parameters, perform the requested task and add only the short ready hint instead of repeating the full tutorial.
- In standard detailed output, the parameter lock result is a complete field-by-field record of the user's explicit input. Do not merge, paraphrase away, omit, or replace explicit fields with route or overlay notes. Add inferred defaults only as clearly labeled supplements. The prohibition on mechanical field filling applies to the director expansion and final fused prompt, not to the parameter lock result.
- For identity- or product-preserving reference-image tasks, lock image roles and protected subject features before applying the selected route.
- In `source_faithful_stylization`, preserve the original identity, facial structure and visible distinguishing features, hairstyle, clothing and accessories, expression, pose, gaze, subject count, viewpoint, perspective, composition, aspect ratio, and existing crop. Change only the requested visual treatment. Do not invent age, ethnicity, an action, background objects, hidden body parts, or uncropped anatomy. Restaging defaults and facial-beauty or ethnicity exclusions from templates cannot override reference facts.
- In `protected_region_edit`, follow the region and capability requirements in `reference-image-lock.md`. Style instructions cannot authorize changes to protected pixels; a reference-guided generation alone cannot establish that the original region is unchanged.
- Use the registries as the only routing entry points. Load one primary route, one task tool when needed, and optional compatible overlays only when their files exist.
- Match the V1.5 / V1.6 Routes by compound fingerprints in [skill/style-registry.md](skill/style-registry.md). Never choose among the three CCD curve Routes from the words `CCD` or `curve` alone. Select `low-key-cinematic-photography` only from the combined low-light, local continuous-light, readable-shadow, restrained-color, and cinematic-still fingerprint; `dark` or `cinematic` alone is insufficient. Never load two primary Routes as a style blend.
- Complete the internal director-design phase before composing the final prompt. For new scenes, expand age cues, facial features, expression, body direction, pose, clothing, palette direction, visual richness, scene, camera, lighting, filter, and platform adaptation into one photographed moment. For preserved photos, carry source facts and locks through these paragraph roles and expand only the permitted treatment.
- For new scenes, build one coherent photographed moment with a time slice, one small event, an action chain, a gaze target, and two or three selective environment details. For preserved photos, describe the existing visible moment and permitted treatment instead; do not add an event or environment detail to satisfy this template.
- Use route templates as visual direction, not as sentence banks. Do not return a summary or mechanically fill fields.
- Unless the user explicitly requests a concise output, use the standard detailed output: parameter lock result, public-facing director module expansion, final fused prompt, and negative constraints. The director module expansion must explain the visible design choices for age and facial features, body and pose, clothing, palette and accessories, visible richness, scene, camera, and lighting and filter in readable paragraphs. Do not reduce it to a short field recap.
- Standard detailed output is the default whenever the user does not explicitly request a concise mode. Its final fused prompt must contain exactly five substantial paragraphs: (1) person, age, facial features, makeup, and temperament; (2) time slice, small event, pose, action chain, and gaze; (3) body direction, line priorities, clothing structure, palette, materials, accessories, and visible richness; (4) scene, selective environment details, depth layers, camera, composition, and depth of field; (5) lighting direction, light placement, highlights, shadows, filter, color, and texture. Do not self-select a shorter format.
- Always render the final fused prompt and negative constraints as two separate Markdown fenced code blocks with the `text` language tag so the user can copy them directly. Keep section titles outside the fences. Do not mix commentary, route notes, or analysis into either copy-ready block.
- Before responding, run an internal parameter-propagation audit. Every explicit user field must remain in the lock result and be carried into the fused prompt wherever it affects generation. `画幅比例`, pixel dimensions, or other size instructions are mandatory prompt controls: place them in the first sentence of the copy-ready prompt, using the user's exact value when provided. For preserved photos, inherit the source dimensions, ratio, and crop instead of supplementing a new format; conflicting size or crop instructions must be resolved under `reference-image-lock.md`.
- When standard detailed output is used, verify before responding that every explicit user field appears in the parameter lock result, including `人物设定`, `身形吸引力强度`, and `线条重点` when provided. Route and overlay IDs may be listed only as supplemental notes.
- Keep private chain-of-thought internal. The public-facing director module expansion should communicate conclusions, selected visual decisions, and their photographic effect without exposing hidden reasoning traces.
- Default new text-only scenes without identity references to fictional, clearly adult subjects. Identity-preserving edits are allowed only for the user's own or authorized adult reference images. Adult sensual or curve-focused portrait requests may preserve visual attraction, but must avoid exposed nipples, exposed genitals, explicit sexual acts, and any minor or ambiguous-age framing.
- Treat a bare portrait parameter block as a prompt-generation request, never as an implicit request to generate an image. If `输出模式` is omitted, always use the standard detailed prompt output. Invoke image generation only when the user explicitly requests `直接生成图片` or uses equivalent direct wording such as "直接出图" or "生成图片".
- If the user requests `只要最终提示词`, output only the final prompt and negative constraints.
- If the user requests direct image generation, prepare the directed prompt internally and route it to the available image-generation capability.
- An uploaded image does not override an explicit request for analysis or prompts only. For `只要最终提示词` or equivalent, apply the same reference locks to the prompt and negative constraints, without calling image generation; text alone cannot guarantee identity, geometry, or unchanged pixels.
- If the user uploads reference images and explicitly asks to generate or edit an image while preserving a person or product, use the reference-image direct-generation tool. Verify an available capability can accept every required reference and enforce the requested preservation mode before calling it. Return an image only after actual generation; never claim the Skill itself supplies an image editor.

## Public references

- Quick-start and first-call help: [skill/help.md](skill/help.md)
- Usage guide: [skill/public_instructions.md](skill/public_instructions.md)
- Parameter schema: [skill/parameter_schema.md](skill/parameter_schema.md)
- Safety summary: [docs/prompt_safety.md](docs/prompt_safety.md)
- Examples: [examples](examples)
- Version notes: [docs/versioning.md](docs/versioning.md)

Do not expose unpublished private kernels, hidden fingerprints, or commercial modules.
