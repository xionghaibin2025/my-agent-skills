# Nature Journal Fragment

## Style Combination

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'nature'])
```

## What `nature` overrides

| Parameter | Value | Reason |
|---|---|---|
| `figure.figsize` | `3.3, 2.5` | Nature single-column width (89 mm ≈ 3.5 in) |
| `font.family` | `sans-serif` | Nature uses sans-serif (Helvetica/Arial) |
| `font.size` | `7` | Nature's preferred figure font size |

## Nature-Specific Guidelines

1. **Sans-serif fonts are mandatory**. The `nature` style switches from serif
   to sans-serif automatically.
2. **Single-column width**: 89 mm (≈3.5 in) — the default `nature` figsize.
3. **Double-column width**: 183 mm (≈7.2 in) — override figsize manually.
4. **Resolution**: minimum 300 DPI, 600 DPI recommended.
5. **File formats**: PDF or EPS preferred; TIFF for photographs.

## Recommended Color Cycles for Nature

```python
# Vibrant colors (Nature's typical look)
plt.style.use(['science', 'nature', 'vibrant'])

# Bright colors (good contrast)
plt.style.use(['science', 'nature', 'bright'])

# Muted tones (for many data series, up to 10 colors)
plt.style.use(['science', 'nature', 'muted'])
```

## Export Template

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'nature'])

fig, ax = plt.subplots()
# ... your plot code ...

# Save for Nature submission
fig.savefig('figure1.pdf', dpi=600, bbox_inches='tight')
fig.savefig('figure1.tiff', dpi=300, bbox_inches='tight')  # photographs
fig.savefig('figure1.svg', bbox_inches='tight')  # vector (editable)
```

## Multi-Panel Layout for Nature

```python
import matplotlib.pyplot as plt
import scienceplots
import matplotlib.gridspec as gridspec

plt.style.use(['science', 'nature', 'vibrant'])

# Full-width 3-panel figure
fig = plt.figure(figsize=(7.2, 2.5))
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

# Add panel labels (a, b, c)
for ax, label in zip([ax1, ax2, ax3], ['a', 'b', 'c']):
    ax.text(-0.15, 1.05, f'\\textbf{{{label}}}', transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='bottom')

# ... your plot code ...
fig.savefig('figure_multipanel.pdf', dpi=600, bbox_inches='tight')
```

## Nature Figure Size Reference

| Layout | Width (mm) | Width (in) | figsize example |
|---|---|---|---|
| Single column | 89 | 3.5 | `(3.5, 2.5)` |
| 1.5 columns | 120 | 4.7 | `(4.7, 3.5)` |
| Double column | 183 | 7.2 | `(7.2, 3.0)` |
| Full page | 183 × 247 | 7.2 × 9.7 | `(7.2, 9.7)` |
