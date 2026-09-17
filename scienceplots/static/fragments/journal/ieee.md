# IEEE Journal Fragment

## Style Combination

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])
```

## What `ieee` overrides

| Parameter | Value | Reason |
|---|---|---|
| `figure.figsize` | `3.3, 2.5` | Fits IEEE single-column width (≈3.5 in / 88.9 mm) |
| `figure.dpi` | `600` | IEEE requires ≥600 DPI for print |
| `font.family` | `serif` | IEEE uses Times/serif fonts |
| `font.size` | `8` | Standard for IEEE column text |

## IEEE-Specific Guidelines

1. **Figures must be readable in black-and-white**. Use the `ieee` style which
   produces B/W-friendly figures, or combine with `high-contrast` color cycle.
2. **Single-column figures**: default `ieee` width.
3. **Double-column figures**: override figsize to `(7.0, 3.5)`.
4. **Resolution**: minimum 600 DPI for all figures.

## Recommended Color Cycles for IEEE

```python
# Black-and-white friendly (safest)
plt.style.use(['science', 'ieee'])

# If color is acceptable
plt.style.use(['science', 'ieee', 'bright'])

# High contrast (3 colors only, very B/W safe)
plt.style.use(['science', 'ieee', 'high-contrast'])
```

## Export Template

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

fig, ax = plt.subplots()
# ... your plot code ...

# Save for IEEE submission
fig.savefig('figure1.pdf', dpi=600, bbox_inches='tight')
fig.savefig('figure1.png', dpi=600, bbox_inches='tight')  # fallback
```

## Double-Column Override

```python
plt.style.use(['science', 'ieee'])

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.5))
# ... your plot code ...
fig.savefig('figure_double_col.pdf', dpi=600, bbox_inches='tight')
```
