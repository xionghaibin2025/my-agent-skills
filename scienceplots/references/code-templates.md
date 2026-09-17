# SciencePlots Code Templates Reference

Ready-to-copy Python code templates for common scientific plot types.
Every template is self-contained—copy, paste, adjust data, and run.

---

## Table of Contents

1. [Single Panel Line Plot](#1-single-panel-line-plot)
2. [Multi-Panel Subplot Grid](#2-multi-panel-subplot-grid)
3. [Bar Chart with Error Bars](#3-bar-chart-with-error-bars)
4. [Scatter Plot with Colorbar](#4-scatter-plot-with-colorbar)
5. [Histogram / Distribution Plot](#5-histogram--distribution-plot)
6. [Heatmap / Contour Plot](#6-heatmap--contour-plot)
7. [Box Plot / Violin Plot](#7-box-plot--violin-plot)
8. [Dual Y-Axis Plot](#8-dual-y-axis-plot)
9. [Inset Plot (Zoom-In)](#9-inset-plot-zoom-in)
10. [Legend Customization](#10-legend-customization)
11. [Saving in Multiple Formats](#11-saving-in-multiple-formats)

---

## 1. Single Panel Line Plot

The simplest and most common scientific figure—a single Axes with one or
more data series.

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

# Activate the SciencePlots 'science' style
# Combine with 'no-latex' if LaTeX is not installed
plt.style.use(['science'])
# plt.style.use(['science', 'no-latex'])  # fallback without LaTeX

# --- Generate sample data ---
x = np.linspace(0, 2 * np.pi, 200)
y1 = np.sin(x)
y2 = np.cos(x)

# --- Create figure ---
fig, ax = plt.subplots(
    figsize=(3.5, 2.625),  # single-column width (inches) for most journals
    dpi=150,               # screen preview DPI; save DPI is set separately
)

# Plot data series
ax.plot(x, y1, label=r'$\sin(x)$')          # raw string for LaTeX math
ax.plot(x, y2, label=r'$\cos(x)$', ls='--') # dashed line style

# Labels & title
ax.set_xlabel(r'$x$ (rad)')
ax.set_ylabel(r'$f(x)$')
ax.set_title('Trigonometric Functions')

# Legend
ax.legend(loc='best', frameon=True)

# Axis limits (optional)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.2, 1.2)

# --- Save ---
fig.savefig('single_panel.pdf', dpi=300, bbox_inches='tight')
fig.savefig('single_panel.png', dpi=600, bbox_inches='tight')
plt.show()
```

---

## 2. Multi-Panel Subplot Grid

### 2×2 Grid

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

x = np.linspace(0, 4 * np.pi, 300)

# --- Create 2×2 grid ---
fig, axes = plt.subplots(
    nrows=2, ncols=2,
    figsize=(7, 5.25),         # double-column width
    constrained_layout=True,   # automatic spacing (preferred over tight_layout)
)

functions = [np.sin, np.cos, np.tan, lambda t: np.sinc(t / np.pi)]
titles = [r'$\sin(x)$', r'$\cos(x)$', r'$\tan(x)$', r'$\mathrm{sinc}(x)$']

for ax, func, title in zip(axes.flat, functions, titles):
    y = func(x)
    y = np.clip(y, -5, 5)     # clip extreme values for tan
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$f(x)$')

# Panel labels: (a), (b), (c), (d)
for idx, ax in enumerate(axes.flat):
    label = chr(ord('a') + idx)
    ax.text(
        -0.15, 1.05, f'({label})',
        transform=ax.transAxes,
        fontsize=10, fontweight='bold',
        va='bottom', ha='right',
    )

fig.savefig('subplot_2x2.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

### 1×3 Row Layout

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

fig, axes = plt.subplots(
    nrows=1, ncols=3,
    figsize=(7, 2.5),
    sharey=True,               # share y-axis across panels
    constrained_layout=True,
)

x = np.linspace(0, 2 * np.pi, 200)

for i, ax in enumerate(axes):
    ax.plot(x, np.sin(x + i * np.pi / 3), label=f'Phase {i}')
    ax.set_xlabel(r'$x$')
    ax.legend(loc='upper right', fontsize=6)

axes[0].set_ylabel(r'$y$')    # only leftmost panel gets y-label

fig.savefig('subplot_1x3.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 3. Bar Chart with Error Bars

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample data ---
categories = ['A', 'B', 'C', 'D', 'E']
means_1 = [3.2, 4.1, 2.8, 5.0, 3.7]
means_2 = [2.9, 3.5, 3.1, 4.2, 4.0]
errors_1 = [0.3, 0.5, 0.2, 0.4, 0.3]
errors_2 = [0.4, 0.3, 0.3, 0.5, 0.2]

x = np.arange(len(categories))
width = 0.35                   # bar width

fig, ax = plt.subplots(figsize=(3.5, 2.625))

# Grouped bars with error bars
bars1 = ax.bar(
    x - width / 2, means_1, width,
    yerr=errors_1,
    label='Method 1',
    capsize=2,                 # error bar cap width in points
    error_kw={'linewidth': 0.8},
)
bars2 = ax.bar(
    x + width / 2, means_2, width,
    yerr=errors_2,
    label='Method 2',
    capsize=2,
    error_kw={'linewidth': 0.8},
)

ax.set_xlabel('Category')
ax.set_ylabel('Performance')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.set_ylim(0, 6.5)

fig.savefig('bar_chart.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 4. Scatter Plot with Colorbar

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample data ---
rng = np.random.default_rng(42)
n = 200
x = rng.normal(0, 1, n)
y = rng.normal(0, 1, n)
colors = np.sqrt(x**2 + y**2)     # color = distance from origin
sizes = np.abs(x * y) * 80 + 10   # optional: variable marker size

fig, ax = plt.subplots(figsize=(3.5, 3.0))

sc = ax.scatter(
    x, y,
    c=colors,                      # array mapped to colormap
    s=sizes,                       # marker sizes in points²
    cmap='viridis',                # colormap name
    edgecolors='k',                # marker edge color
    linewidths=0.3,                # marker edge width
    alpha=0.85,                    # transparency
)

# Colorbar
cbar = fig.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label(r'$\sqrt{x^2 + y^2}$')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title('Scatter with Colorbar')

fig.savefig('scatter_colorbar.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 5. Histogram / Distribution Plot

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample data ---
rng = np.random.default_rng(0)
data_a = rng.normal(loc=0.0, scale=1.0, size=1000)
data_b = rng.normal(loc=1.5, scale=0.8, size=1000)

fig, axes = plt.subplots(1, 2, figsize=(7, 2.625), constrained_layout=True)

# --- Left: Overlapping histograms ---
ax = axes[0]
ax.hist(data_a, bins=30, density=True, alpha=0.7, label='Group A')
ax.hist(data_b, bins=30, density=True, alpha=0.7, label='Group B')
ax.set_xlabel(r'$x$')
ax.set_ylabel('Probability Density')
ax.legend()
ax.set_title('Histogram')

# --- Right: Cumulative distribution ---
ax = axes[1]
sorted_a = np.sort(data_a)
sorted_b = np.sort(data_b)
cdf = np.arange(1, len(sorted_a) + 1) / len(sorted_a)
ax.plot(sorted_a, cdf, label='Group A')
ax.plot(sorted_b, cdf, label='Group B')
ax.set_xlabel(r'$x$')
ax.set_ylabel('CDF')
ax.legend(loc='lower right')
ax.set_title('Cumulative Distribution')

fig.savefig('histogram.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 6. Heatmap / Contour Plot

### Heatmap (imshow)

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample 2-D data ---
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) * np.exp(-(X**2 + Y**2) / 8)

fig, ax = plt.subplots(figsize=(3.5, 3.0))

im = ax.imshow(
    Z,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',            # (0,0) at bottom-left
    cmap='RdBu_r',             # diverging colormap for ± data
    aspect='equal',
)

cbar = fig.colorbar(im, ax=ax, shrink=0.85)
cbar.set_label(r'$f(x,y)$')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title('Heatmap')

fig.savefig('heatmap.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

### Contour Plot

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots(figsize=(3.5, 3.0))

# Filled contour
cf = ax.contourf(X, Y, Z, levels=20, cmap='coolwarm')
# Contour lines on top
cs = ax.contour(X, Y, Z, levels=10, colors='k', linewidths=0.4)
ax.clabel(cs, inline=True, fontsize=6)   # inline contour labels

cbar = fig.colorbar(cf, ax=ax)
cbar.set_label(r'$\sin(x)\cos(y)$')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')

fig.savefig('contour.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 7. Box Plot / Violin Plot

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample data ---
rng = np.random.default_rng(42)
data = [rng.normal(loc=mu, scale=0.8, size=100) for mu in [2, 3, 3.5, 4]]
labels = ['Ctrl', 'Drug A', 'Drug B', 'Drug C']

fig, axes = plt.subplots(1, 2, figsize=(7, 2.625), constrained_layout=True)

# --- Left: Box plot ---
ax = axes[0]
bp = ax.boxplot(
    data,
    labels=labels,
    patch_artist=True,             # fill boxes with color
    widths=0.5,
    boxprops=dict(linewidth=0.8),
    medianprops=dict(color='black', linewidth=1),
    flierprops=dict(marker='o', markersize=3, alpha=0.5),
)
# Color each box
colors_box = plt.cm.Set2(np.linspace(0, 1, len(data)))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)

ax.set_ylabel('Response')
ax.set_title('Box Plot')

# --- Right: Violin plot ---
ax = axes[1]
vp = ax.violinplot(
    data,
    positions=range(1, len(data) + 1),
    showmeans=True,
    showmedians=True,
)
# Color each violin body
for body, color in zip(vp['bodies'], colors_box):
    body.set_facecolor(color)
    body.set_alpha(0.7)

ax.set_xticks(range(1, len(data) + 1))
ax.set_xticklabels(labels)
ax.set_ylabel('Response')
ax.set_title('Violin Plot')

fig.savefig('box_violin.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 8. Dual Y-Axis Plot

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

# --- Sample data ---
x = np.linspace(0, 10, 100)
y1 = np.exp(-0.3 * x) * np.sin(2 * x)   # decaying oscillation
y2 = 1 - np.exp(-0.5 * x)               # saturation curve

fig, ax1 = plt.subplots(figsize=(3.5, 2.625))

# Left y-axis
color1 = '#0C5DA5'
ax1.set_xlabel(r'Time $t$ (s)')
ax1.set_ylabel(r'Amplitude $A(t)$', color=color1)
line1 = ax1.plot(x, y1, color=color1, label=r'$A(t)$')
ax1.tick_params(axis='y', labelcolor=color1)

# Right y-axis (shares x-axis)
ax2 = ax1.twinx()
color2 = '#FF2C00'
ax2.set_ylabel(r'Concentration $C(t)$', color=color2)
line2 = ax2.plot(x, y2, color=color2, ls='--', label=r'$C(t)$')
ax2.tick_params(axis='y', labelcolor=color2)

# Combined legend from both axes
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right')

fig.savefig('dual_yaxis.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 9. Inset Plot (Zoom-In)

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

plt.style.use(['science'])

# --- Sample data ---
x = np.linspace(0, 6 * np.pi, 1000)
y = np.sin(x) * np.exp(-0.1 * x)

fig, ax = plt.subplots(figsize=(3.5, 2.625))
ax.plot(x, y)
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title('Damped Sine Wave')

# --- Inset axes ---
# width / height as percentage of parent, loc = Matplotlib location code
ax_inset = inset_axes(
    ax,
    width='40%',               # inset width  (% of parent width)
    height='35%',              # inset height (% of parent height)
    loc='upper right',         # position inside the parent
    borderpad=1.5,
)

# Zoom region
x1, x2 = 8, 12
ax_inset.plot(x, y)
ax_inset.set_xlim(x1, x2)
y_region = y[(x >= x1) & (x <= x2)]
margin = 0.05 * (y_region.max() - y_region.min())
ax_inset.set_ylim(y_region.min() - margin, y_region.max() + margin)
ax_inset.tick_params(labelsize=6)

# Draw connector lines between main axes and inset
mark_inset(ax, ax_inset, loc1=2, loc2=4, fc='none', ec='0.5', lw=0.6)

fig.savefig('inset_zoom.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 10. Legend Customization

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(['science'])

x = np.linspace(0, 2 * np.pi, 200)
fig, axes = plt.subplots(2, 2, figsize=(7, 5), constrained_layout=True)

# ---- (a) Basic legend positions ----
ax = axes[0, 0]
for i in range(4):
    ax.plot(x, np.sin(x + i * 0.5), label=f'Series {i+1}')
ax.legend(
    loc='upper right',        # common locations: 'best','upper left','lower right'
    frameon=True,              # draw frame around legend
    fancybox=False,            # square corners (True = rounded)
    edgecolor='black',
    fontsize=6,
)
ax.set_title('(a) Basic Legend')

# ---- (b) Multi-column legend ----
ax = axes[0, 1]
for i in range(6):
    ax.plot(x, np.sin(x + i * 0.4), label=f'$\\phi={i*0.4:.1f}$')
ax.legend(
    ncol=3,                    # number of columns
    loc='upper center',
    fontsize=5,
    columnspacing=0.8,         # space between columns
    handlelength=1.5,          # length of legend line handle
)
ax.set_title('(b) Multi-Column')

# ---- (c) Legend outside the axes ----
ax = axes[1, 0]
for i in range(4):
    ax.plot(x, np.cos(x + i * 0.5), label=f'Case {i+1}')
ax.legend(
    bbox_to_anchor=(1.05, 1), # (x, y) in axes coordinates; >1 = outside
    loc='upper left',
    borderaxespad=0,
    fontsize=6,
)
ax.set_title('(c) Outside Legend')

# ---- (d) Custom markers in legend ----
ax = axes[1, 1]
ax.plot(x, np.sin(x), 'o-', markevery=20, markersize=3, label='Experiment')
ax.plot(x, np.sin(x) * 0.9, '--', label='Model')
ax.fill_between(
    x, np.sin(x) * 0.85, np.sin(x) * 0.95,
    alpha=0.3, label=r'$\pm 5\%$ CI',
)
ax.legend(fontsize=6)
ax.set_title('(d) Custom Markers')

fig.savefig('legend_examples.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 11. Saving in Multiple Formats

```python
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import os

plt.style.use(['science'])

# --- Create a sample figure ---
x = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots(figsize=(3.5, 2.625))
ax.plot(x, np.sin(x), label=r'$\sin(x)$')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.legend()

# --- Output directory ---
output_dir = 'figures'
os.makedirs(output_dir, exist_ok=True)

# ---------- PDF (vector, best for journals) ----------
fig.savefig(
    os.path.join(output_dir, 'figure.pdf'),
    dpi=300,                   # ignored for vector, but sets rasterized element DPI
    bbox_inches='tight',      # crop whitespace
    pad_inches=0.02,          # small padding around the figure
    transparent=False,        # True for transparent background
)

# ---------- PNG (raster, good for web / slides) ----------
fig.savefig(
    os.path.join(output_dir, 'figure.png'),
    dpi=600,                   # 600 DPI for print quality
    bbox_inches='tight',
    transparent=False,
)

# ---------- SVG (vector, web-friendly) ----------
fig.savefig(
    os.path.join(output_dir, 'figure.svg'),
    bbox_inches='tight',
    transparent=False,
)

# ---------- TIFF (raster, some journals require this) ----------
fig.savefig(
    os.path.join(output_dir, 'figure.tiff'),
    dpi=600,
    bbox_inches='tight',
    pil_kwargs={
        'compression': 'tiff_lzw',  # lossless compression → smaller file
    },
)

# ---------- EPS (vector, legacy format) ----------
fig.savefig(
    os.path.join(output_dir, 'figure.eps'),
    bbox_inches='tight',
)

plt.show()

print(f'Figures saved to {os.path.abspath(output_dir)}/')
```

### Quick-Reference: DPI Guidelines

| Use Case                  | Recommended DPI | Format       |
|---------------------------|-----------------|--------------|
| Journal submission        | 300–600         | PDF or TIFF  |
| High-res print            | 600             | PNG or TIFF  |
| Slides / presentations    | 150–300         | PNG          |
| Web / README              | 150             | PNG or SVG   |
| Archival / vector editing | N/A (vector)    | PDF, SVG, EPS|

---

## Tips

- **`bbox_inches='tight'`** – Always use this to avoid clipped labels.
- **`constrained_layout=True`** – Preferred over `plt.tight_layout()` for
  subplots; avoids overlapping labels automatically.
- **`plt.style.use(['science', 'ieee'])`** – Combine styles for
  journal-specific formatting.
- **`plt.style.use(['science', 'no-latex'])`** – Use when LaTeX is not
  installed.
- **Raw strings `r'...'`** – Always use raw strings for LaTeX math in labels
  to prevent Python escape-sequence issues.
