# SciencePlots — Complete Styles Catalog

## Base Styles

### `science` — Primary Base Style
- **Location**: `styles/science.mplstyle`
- **Purpose**: Core scientific plotting style — serif fonts, LaTeX rendering, inward ticks, thin lines, high DPI (600), small figure size for journal columns.
- **Usage**: `plt.style.use('science')`
- **Note**: This is the foundation. All other styles are designed to cascade on top of it.

### `scatter` — Scatter Plot Optimizations
- **Location**: `styles/scatter.mplstyle`
- **Purpose**: Adjusts marker sizes and line settings optimized for scatter plots.
- **Usage**: `plt.style.use(['science', 'scatter'])`

---

## Journal Styles (`styles/journals/`)

### `ieee` — IEEE Transactions
- **Purpose**: Single-column width (3.3 in), 600 DPI, serif fonts (Times). Figures are readable in B/W.
- **Usage**: `plt.style.use(['science', 'ieee'])`
- **Overrides**: `figure.figsize`, `figure.dpi`, font settings

### `nature` — Nature Journals
- **Purpose**: Single-column width (89 mm), sans-serif fonts (Helvetica/Arial), smaller font sizes.
- **Usage**: `plt.style.use(['science', 'nature'])`
- **Overrides**: `font.family` → `sans-serif`, font sizes

---

## Color Cycle Styles (`styles/color/`)

All color styles **only** change the color cycle (`axes.prop_cycle`). They do not modify fonts, sizes, or layout.

### Paul Tol's Color-Blind Safe Schemes

| Style | # Colors | Description |
|---|---|---|
| `bright` | 7 | Vivid, high-contrast, color-blind safe |
| `vibrant` | 7 | Saturated, modern palette |
| `muted` | 10 | Soft, muted tones for many data series |
| `high-contrast` | 3 | Maximum contrast, B/W safe, only 3 colors |
| `light` | 9 | Light/pastel colors |

```python
# Example
plt.style.use(['science', 'bright'])
```

### Other Color Schemes

| Style | # Colors | Description |
|---|---|---|
| `high-vis` | 4 | Maximum visibility, bold colors |
| `retro` | 6 | Vintage/classic color palette |
| `std-colors` | 10 | Reverts to default Matplotlib color cycle |

### Discrete Rainbow Series

For exact color count control, use `discrete-rainbow-N` where N = 1 to 23:

| Style | Colors |
|---|---|
| `discrete-rainbow-1` | 1 color |
| `discrete-rainbow-2` | 2 colors |
| `discrete-rainbow-3` | 3 colors |
| ... | ... |
| `discrete-rainbow-23` | 23 colors |

```python
# Use exactly 5 distinct colors
plt.style.use(['science', 'discrete-rainbow-5'])

# Use exactly 10 distinct colors
plt.style.use(['science', 'discrete-rainbow-10'])
```

---

## Language / Font Styles (`styles/languages/`)

> **Note**: CJK font styles are deprecated in favor of the `mplfonts` package.
> However, they still work and are useful for quick setup.

| Style | Language | Font |
|---|---|---|
| `cjk-sc-font` | Simplified Chinese (简体中文) | Noto Sans CJK SC |
| `cjk-tc-font` | Traditional Chinese (繁體中文) | Noto Sans CJK TC |
| `cjk-jp-font` | Japanese (日本語) | Noto Sans CJK JP |
| `cjk-kr-font` | Korean (한국어) | Noto Sans CJK KR |
| `russian-font` | Russian (Русский) | — |
| `turkish-font` | Turkish (Türkçe) | — |

**Important**: Always combine with `no-latex` when using language styles:
```python
plt.style.use(['science', 'no-latex', 'cjk-sc-font'])
```

---

## Miscellaneous Styles (`styles/misc/`)

| Style | Purpose | Usage |
|---|---|---|
| `grid` | Adds major grid lines to the plot | `['science', 'grid']` |
| `no-latex` | Disables LaTeX text rendering. **Required** when LaTeX is not installed or when using CJK fonts | `['science', 'no-latex']` |
| `notebook` | Larger figure size and fonts for Jupyter notebooks | `['science', 'notebook']` |
| `latex-sans` | Uses LaTeX with sans-serif fonts (via `sansmath` package) | `['science', 'latex-sans']` |
| `pgf` | Uses PGF backend for direct LaTeX document integration | `['science', 'pgf']` |

---

## Style Combination Quick Reference

| Goal | Style Combination |
|---|---|
| Basic paper figure | `['science']` |
| IEEE submission | `['science', 'ieee']` |
| Nature submission | `['science', 'nature']` |
| Notebook display | `['science', 'notebook']` |
| No LaTeX | `['science', 'no-latex']` |
| With grid | `['science', 'grid']` |
| Color-blind safe | `['science', 'bright']` or `['science', 'vibrant']` |
| B/W safe | `['science', 'high-contrast']` |
| Chinese labels | `['science', 'no-latex', 'cjk-sc-font']` |
| IEEE + vibrant colors | `['science', 'ieee', 'vibrant']` |
| Nature + bright colors | `['science', 'nature', 'bright']` |
| Notebook + grid | `['science', 'notebook', 'grid']` |
| Presentation (large, colorful) | `['science', 'no-latex', 'notebook', 'vibrant']` |
| Scatter with muted colors | `['science', 'scatter', 'muted']` |
| Sans-serif LaTeX | `['science', 'latex-sans']` |
| Embed in LaTeX doc (PGF) | `['science', 'pgf']` |
