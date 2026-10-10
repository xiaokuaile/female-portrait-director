[English](README.md) | [简体中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)

# 女性人像提示词导演 Skill

输入少量写真参数，生成一份人物、动作、服装、场景、镜头与光线彼此成立的提示词。宿主连接合适的图像工具时，也可以编排直接出图或授权参考图编辑。

[![skills.sh](https://skills.sh/b/liyue-aigc/female-portrait-director)](https://skills.sh/liyue-aigc/female-portrait-director)
[![GitHub stars](https://img.shields.io/github/stars/liyue-aigc/female-portrait-director?style=flat)](https://github.com/liyue-aigc/female-portrait-director/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

它不是普通提示词合集。Skill 会锁定用户的明确要求，只选择一个视觉 Route，再把人物、事件、服装、空间、镜头、光线和滤镜组织成同一个可拍摄瞬间。没有授权参考图时，人物默认为虚构且明确成年的女性。

## 先看结果

| 清纯生活 | 都市时尚 | 古风仙侠 |
| --- | --- | --- |
| ![咖啡馆窗边清纯生活照](assets/cases/01-clean-lifestyle.png) | ![商场外都市时尚街拍](assets/cases/02-urban-fashion.png) | ![红金华服古风仙侠写真](assets/cases/03-gufeng-xianxia.png) |
| 港风街拍 | 法式慵懒 | 纯欲曲线 |
| ![夕阳老街港风写真](assets/cases/04-retro-hongkong-street.png) | ![巴黎阳台法式慵懒写真](assets/cases/05-french-lazy.png) | ![清透生活感纯欲曲线写真](assets/cases/06-pure-desire-curve.png) |

六个案例依次展示：清纯生活、都市时尚、古风仙侠、港风街拍、法式慵懒和纯欲曲线。

## 60 秒开始使用

使用开源 `skills` CLI 一键安装：

```bash
npx skills@1.7.2 add https://github.com/xiaokuaile/female-portrait-director/tree/main/skills/female-portrait-director --skill female-portrait-director --agent codex --copy -g
```

重新开始一个 Agent 对话，然后粘贴：

```text
使用 $female-portrait-director 直接生成图片：
风格：清纯生活照
场景：午后安静的咖啡馆靠窗座位
服装：米白针织开衫 + 浅色内搭
气质：温柔、自然、明确成年
画幅：3:4
```

如果只需要可复制提示词，删除“直接生成图片”即可。Skill 会返回参数锁定、导演式提示词和负面约束。

## Agent 兼容性

上游发布说明记录了完整分发包在 `skills` CLI 中针对以下目标端的安装验证：

| Agent | 安装包 | 提示词工作流 | 直接生图工作流 |
| --- | --- | --- | --- |
| Codex | 上游已验证 | 上游环境已运行 | 取决于宿主图像工具及其编辑能力 |
| Claude Code | 上游已验证 | 兼容 Agent Skills | 取决于所连接的生图工具 |
| Cursor | 上游已验证 | 兼容 Agent Skills | 取决于所连接的生图工具 |
| GitHub Copilot | 上游已验证 | 兼容 Agent Skills | 取决于所连接的生图工具 |
| Gemini CLI | 上游已验证 | 兼容 Agent Skills | 取决于所连接的生图工具 |

“安装包已验证”表示安装器会把 `SKILL.md` 及其引用模块复制到目标 Skill。上表的实际运行结论属于上游发布环境，不能证明另一台设备已经安装、具备图像工具或通过照片编辑保真验收。本仓库提供 Markdown 指令，不内置图像模型或编辑引擎。提示词、图像工具执行、成图保真是三层独立验收，详见[验证方法](docs/reference-fidelity-validation.md)。

## 支持风格

- 清纯生活照
- 纯欲曲线生活照
- 都市时尚写真
- 古风仙侠美人图
- 电商服装模特图
- 复古港风写真
- 法式慵懒写真
- 新中式东方写真
- 活力运动写真
- 旅行假日写真
- 影楼精修写真
- 东方丰腴写真
- 清冷仙气古风增强版
- 明媚华贵古风增强版
- 超近景真实人脸人像
- 古风贵女水光妆
- 黑珍珠墨金CCD曲线生活照
- 元气丰腴柔光CCD生活照
- 冷白清透CCD曲线生活照
- 低调电影感摄影

完整的新手教学、20 风格菜单和参数转五段式详细提示词示例见 [首次使用帮助](skill/help.md)。

## 核心能力

- 锁定用户已经填写的参数，只做细化和稳定化补全。
- 根据目标风格按需加载单一路由，避免互相冲突的风格词堆叠。
- 拆解五官、身形、服装、场景、镜头姿态、光线和滤镜模块。
- 将短参数扩写为可拍摄的具体瞬间，避免机械复述和填空式输出。
- 将各模块融合为自然、完整、可直接复制的摄影导演式提示词。
- 为电商图片保留服装展示优先级，为曲线风格保留明确的安全边界。
- 使用明确的保真规则编排授权参考图生成与编辑。

## 照片保真与能力边界

此 fork 保留李岳的原作，并加强照片保真默认规则。照片风格转换默认使用 `source_faithful_stylization`，锁定原人物身份、面部特征、发型、服装、姿态与动作、主体数量、拍摄角度、构图和裁切。只改变用户要求的色彩、光影表现或渲染风格，风格 Route 不得自行换脸、换装或重构画面。

可选的 `参考图模式` 有 `source_faithful_stylization`、`identity_restage`（只重排用户明确允许改变的项目）和 `protected_region_edit`。旧参数继续有效；需要时可补充允许改变、保护区域和原图尺寸，未填写新字段不意味着解除保护。上传图片后明确说“只要提示词”，仍只输出提示词。

“原图不变”若要求原区域像素完全相同，`protected_region_edit` 必须使用确定性保护，例如保存并回贴编辑遮罩以外的原像素，再对保护区域做逐像素验证。生成式提示词本身不能保证原区域不变。宿主工具无法支持这套流程时，应在生成前说明限制，并按用户要求提供提示词或编辑方案。详见[参考图规则](skill/core/reference-image-lock.md)。

## 安装与更新

此处核实的 CLI 版本为 `skills@1.7.2`，需要 [Node.js](https://nodejs.org/) `>=22.20.0` 并包含 `npx`。这里的命令安装此 fork；[原上游仓库](https://github.com/liyue-aigc/female-portrait-director)仍为作者原作。更新已有安装前，先备份本地修改，并确认安装记录指向预期的 fork 和版本。直接更新一个追踪上游的安装不会取得此 fork 的保真规则。CLI 管理的全局安装可使用以下指定技能的更新命令：

```bash
npx skills@1.7.2 update female-portrait-director -g
```

在 `skills@1.7.2` 中，名称限定此 Skill，`-g` 限定全局范围；当前项目安装改用 `-p`。省略名称可能更新所选范围内全部已追踪技能。更新会沿用记录的来源并重新安装，可能替换本地修改；去掉 `-y` 不会变成预览，也不保证逐项覆盖前确认。`update` 不提供 `--agent` 筛选。执行前须核对来源并备份，详见[官方 CLI 更新说明](https://github.com/vercel-labs/skills/blob/671e8c320810d36fed80fac5f1a2c1bf7e82d812/README.md#skills-update)。

### 使用 Git 手动安装到 Codex

也可以将完整仓库克隆到一个新的 Codex Skill 目录，根 `SKILL.md`、`skill/`、`docs/` 和 `agents/` 应一起保留。CLI 安装的是自包含的 `skills/female-portrait-director/` 分发目录。不要只复制 `SKILL.md`，也不要覆盖含本地配置的已有目录；已有安装应审查后合并，详见[安装验证](docs/reference-fidelity-validation.md)。

Windows PowerShell：

```powershell
git clone https://github.com/xiaokuaile/female-portrait-director.git "$env:USERPROFILE\.codex\skills\female-portrait-director"
```

macOS 或 Linux：

```bash
git clone https://github.com/xiaokuaile/female-portrait-director.git "${CODEX_HOME:-$HOME/.codex}/skills/female-portrait-director"
```

重启 Codex 或重新开始一个对话，然后调用：

```text
$female-portrait-director
```

首次无参数调用会显示 V1.6 教程：20 种已实现风格、基础与高级模板、风格 + 气质组合规则、参数生成详细提示词示例，以及直接出图与授权参考图用法。

## 示例：从参数到导演式扩写

这个 Skill 不只是复述用户输入。它会保留明确参数，补全缺失的视觉细节，并输出参数锁定结果、导演式模块解析、完整提示词和负面约束。

```text
写真风格：古风仙侠美人图
场景方向：云雾山水间的古风庭院回廊
服装方向：月白色唐风幻想大袖衫 + 轻盈披帛 + 银色刺绣腰封
气质标签：清冷、疏离、仙气
五官方向：古典东方美人脸
身形方向：纤细清瘦身形
镜头方向：轻侧身站姿，半身到大腿构图
光线氛围：冷调柔光
滤镜效果：清冷仙气古风滤镜
画幅比例：9:16
平台用途：角色写真
```

![古风仙侠参数扩写示例](assets/examples/gufeng-director-output.jpg)

## 输出格式

```text
一、参数锁定结果
二、模块解析
三、最终提示词
四、负面约束
```

## 文件结构

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

## 安全边界

文本生图默认使用虚构、明确成年的人物。参考图工作流允许保留用户本人或已授权成年人物的身份，也允许保留用户有权使用的产品视觉。禁止用于未成年人性化、色情裸露、非自愿图像、欺骗性身份内容、骚扰、诽谤、隐私侵犯或其他违法违规用途。详细规则参见 [prompt_safety.md](docs/prompt_safety.md) 和 [DISCLAIMER.md](DISCLAIMER.md)。

## License

本项目使用 [MIT License](LICENSE)。MIT License 允许使用、复制、修改、合并、发布、分发、再许可和销售副本。安全边界属于合理使用说明，不改变 MIT License 的标准授权范围。

## 作者与版本

- 作者：李岳
- 版本：`FEMALE-PORTRAIT-DIRECTOR-V1.6`
- 项目：`Female Portrait Prompt Director Skill`
