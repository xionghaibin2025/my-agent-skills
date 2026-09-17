# General Scientific Figure Fragment

## Style Combination

```python
import matplotlib.pyplot as plt
import scienceplots

# Basic science style
plt.style.use('science')

# For notebooks / presentations (larger fonts and figure size)
plt.style.use(['science', 'notebook'])

# Without LaTeX
plt.style.use(['science', 'no-latex'])

# With grid lines
plt.style.use(['science', 'grid'])
```

## Common Combinations

### For Papers (generic)
```python
plt.style.use(['science'])  # serif, LaTeX, 3.3×2.5 in
```

### For Jupyter Notebooks
```python
plt.style.use(['science', 'notebook'])  # larger fonts, bigger figure
```

### For Presentations
```python
plt.style.use(['science', 'no-latex', 'notebook', 'bright'])
```

### For LaTeX-Free Environments
```python
plt.style.use(['science', 'no-latex'])
```

### With Grid Lines
```python
plt.style.use(['science', 'grid'])
```

### Scatter Plots
```python
plt.style.use(['science', 'scatter'])
```

### Sans-Serif with LaTeX
```python
plt.style.use(['science', 'latex-sans'])
```

### PGF Backend (for direct LaTeX integration)
```python
plt.style.use(['science', 'pgf'])
```

## Choosing a Color Cycle

Pick the color cycle that matches your needs:

| Style | Colors | Best For |
|---|---|---|
| (default) | 7 | General use |
| `bright` | 7 | Vivid, distinct colors |
| `vibrant` | 7 | Modern, saturated look |
| `muted` | 10 | Many series, soft tones |
| `high-contrast` | 3 | B/W printing, accessibility |
| `light` | 9 | Light pastel colors |
| `high-vis` | 4 | Maximum visibility |
| `retro` | 6 | Vintage/classic look |
| `std-colors` | 10 | Default matplotlib colors |
| `discrete-rainbow-N` | N | Exact number of distinct colors (1–23) |

```python
# Example: science + bright colors
plt.style.use(['science', 'bright'])

# Example: science + exactly 5 distinct colors
plt.style.use(['science', 'discrete-rainbow-5'])
```

## Export Template

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science'])

fig, ax = plt.subplots()
# ... your plot code ...

# Vector format (best for publications)
fig.savefig('figure.pdf', dpi=600, bbox_inches='tight')

# Raster format (for web / slides)
fig.savefig('figure.png', dpi=300, bbox_inches='tight')

# SVG (editable in Illustrator/Inkscape)
fig.savefig('figure.svg', bbox_inches='tight')
```

## Temporary Style Application

Use `plt.style.context()` to apply a style temporarily without affecting
other plots:

```python
with plt.style.context(['science', 'ieee']):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.savefig('ieee_figure.pdf')

# Outside the context, default style is restored
```
