# Style Defaults — The `science` Base Style

The `science` style is the primary/base style in SciencePlots. All other styles
are designed to be **cascaded on top** of it.

## What `science` sets

| Parameter | Value | Purpose |
|---|---|---|
| `text.usetex` | `True` | Uses LaTeX for all text rendering |
| `font.family` | `serif` | Serif font family (professional look) |
| `font.size` | `8` | Base font size suitable for journal columns |
| `axes.labelsize` | `8` | Axis label size |
| `legend.fontsize` | `7` | Legend text size |
| `xtick.labelsize` | `7` | X-axis tick label size |
| `ytick.labelsize` | `7` | Y-axis tick label size |
| `figure.figsize` | `3.3, 2.5` | Single-column width (≈84mm) |
| `figure.dpi` | `600` | High resolution for print |
| `savefig.dpi` | `600` | High resolution on save |
| `lines.linewidth` | `1.0` | Thin lines for clarity |
| `lines.markersize` | `3` | Small markers |
| `axes.linewidth` | `0.5` | Thin axis borders |
| `grid.linewidth` | `0.5` | Thin grid lines |
| `xtick.direction` | `in` | Inward tick marks |
| `ytick.direction` | `in` | Inward tick marks |
| `xtick.major.size` | `3` | Tick length |
| `ytick.major.size` | `3` | Tick length |
| `xtick.minor.visible` | `True` | Show minor ticks |
| `ytick.minor.visible` | `True` | Show minor ticks |
| `legend.frameon` | `False` | No legend border |

## Default Color Cycle

The `science` style uses a curated 10-color cycle designed for good contrast
in both color and black-and-white printing:

```
#0C5DA5 (blue), #00B945 (green), #FF9500 (orange), #FF2C00 (red),
#845B97 (purple), #474747 (gray), #9e9e9e (light gray)
```

## Cascading Behavior

Styles are applied in list order. Later styles override earlier ones:

```python
# Base style only
plt.style.use('science')

# Base + journal formatting
plt.style.use(['science', 'ieee'])

# Base + journal + color scheme
plt.style.use(['science', 'nature', 'bright'])

# Base + no LaTeX + notebook sizing
plt.style.use(['science', 'no-latex', 'notebook'])
```

**Order matters**: always put `science` first, then journal styles, then
color/language/misc styles.
