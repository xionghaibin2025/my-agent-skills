---
name: scienceplots
description: >-
  SciencePlots matplotlib style library skill. Use when the user asks to create
  scientific figures with matplotlib using SciencePlots styles, apply publication-
  quality formatting (science, ieee, nature, grid, notebook, no-latex, bright,
  vibrant, muted, high-contrast, retro, high-vis, CJK fonts, scatter, pgf, etc.),
  combine or cascade mplstyle sheets, or troubleshoot SciencePlots installation
  (LaTeX, CJK fonts). Trigger keywords: SciencePlots, scienceplots, mplstyle,
  science style, 科研绘图样式, matplotlib科研风格, 学术图表样式, 论文绘图风格.
version: 1.0.0
author: Auto-packaged from github.com/garrettj403/SciencePlots
dependencies:
  - python>=3.8
  - matplotlib>=3.4
---

# SciencePlots — Matplotlib Styles for Scientific Plotting

This skill wraps the [SciencePlots](https://github.com/garrettj403/SciencePlots)
library into an actionable workflow for creating publication-quality figures with
Matplotlib.

SciencePlots provides ~47 cascadable `.mplstyle` sheets covering:

| Category | Key Styles |
|---|---|
| Base | `science`, `scatter` |
| Journals | `ieee`, `nature` |
| Colors | `bright`, `vibrant`, `muted`, `high-contrast`, `light`, `high-vis`, `retro`, `std-colors`, `discrete-rainbow-1`…`-23` |
| Languages | `cjk-sc-font`, `cjk-tc-font`, `cjk-jp-font`, `cjk-kr-font`, `russian-font`, `turkish-font` |
| Misc | `grid`, `no-latex`, `notebook`, `latex-sans`, `pgf` |

## Routing Protocol

Follow these steps every time this skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). Also read every file listed under
`always_load`:

- `static/core/setup.md` — installation check and environment setup
- `static/core/style-defaults.md` — default behavior of the `science` base style

### 2. Check SciencePlots installation

Before generating any plotting code, verify the user's environment:

1. Check if `scienceplots` is importable.
2. If not installed, provide the install command (`pip install SciencePlots`).
3. Check LaTeX availability. If LaTeX is unavailable, recommend the `no-latex`
   style as a fallback.
4. If the user needs CJK fonts, point them to the CJK font installation guide.

Use `scripts/install_scienceplots.py` for automated checks when appropriate.

### 3. Determine the target output

Identify the user's target from their request:

- **Journal submission** → load the matching journal fragment under
  `static/fragments/journal/` (e.g., `ieee.md`, `nature.md`, or `general.md`).
- **Notebook / presentation** → use `notebook` style combination.
- **General scientific figure** → use the base `science` style.

### 4. Build the figure code

Apply the loaded material in this order:

1. **Setup** (`static/core/setup.md`) — ensure `import scienceplots` is present.
2. **Style defaults** (`static/core/style-defaults.md`) — apply base `science`
   style rules.
3. **Journal/target fragment** — override with target-specific parameters.

Always include `import scienceplots` before any `plt.style.use(...)` call (required
since SciencePlots v2.0.0).

### 5. Reach for references only when needed

The files under `references/` are deep references. Open them on demand per
the `references.on_demand` table in the manifest — for example:

- `references/styles-catalog.md` for the full list of available styles
- `references/usage-guide.md` for style combination rules
- `references/code-templates.md` for ready-to-use code patterns
- `references/troubleshooting.md` for installation or rendering issues
- `references/api-reference.md` for Matplotlib style API details

## Key Rules

1. **Always `import scienceplots`** before `plt.style.use(...)`.
2. **Styles are cascaded** via a list: `plt.style.use(['science', 'ieee', 'bright'])`.
   Later styles override earlier ones.
3. **`no-latex` is required** when LaTeX is not installed, or when using CJK
   language styles.
4. **Color styles** only set the color cycle; they do not change fonts or layout.
5. **Journal styles** set figure width, DPI, and fonts to match the journal's
   requirements.
