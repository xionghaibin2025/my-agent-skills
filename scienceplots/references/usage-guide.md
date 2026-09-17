# SciencePlots — Usage Guide

## Style Cascading: How It Works

SciencePlots styles are applied through Matplotlib's `plt.style.use()` API.
When you pass a **list** of styles, they are applied left-to-right, with each
subsequent style **overriding** any conflicting `rcParams` set by earlier styles.
Non-conflicting parameters from earlier styles are preserved.

### The Cascading Order

Always follow this order:

```
base → journal → color → language → misc
```

| Position | Category | Examples | What It Controls |
|---|---|---|---|
| 1st | **Base** | `science`, `scatter` | Font, ticks, lines, DPI, figure size, LaTeX |
| 2nd | **Journal** | `ieee`, `nature` | Figure width, DPI, font family/size overrides |
| 3rd | **Color** | `bright`, `vibrant`, `muted` | Color cycle only (`axes.prop_cycle`) |
| 4th | **Language** | `cjk-sc-font`, `russian-font` | Font family, disables LaTeX internally |
| 5th | **Misc** | `grid`, `no-latex`, `notebook` | Grid lines, LaTeX toggle, notebook sizing |

### Example: Understanding Override Order

```python
import matplotlib.pyplot as plt
import scienceplots

# Step-by-step cascade:
# 1. 'science'   → sets figure.figsize=(3.3, 2.5), font.size=8, serif fonts
# 2. 'ieee'      → overrides figure.figsize=(3.3, 2.5) (same), keeps serif
# 3. 'vibrant'   → overrides ONLY axes.prop_cycle (colors), everything else untouched
# 4. 'grid'      → adds axes.grid=True, does not touch fonts or colors

plt.style.use(['science', 'ieee', 'vibrant', 'grid'])
```

### What Happens Under the Hood

Each `.mplstyle` file is a subset of `matplotlib.rcParams`. When you call
`plt.style.use(['A', 'B'])`, Matplotlib does roughly:

```python
plt.rcParams.update(style_A_params)  # Apply A
plt.rcParams.update(style_B_params)  # Apply B — overwrites A's conflicting keys
```

Keys not defined in `B` keep their values from `A`.

---

## Rules for Combining Styles

### What Stacks (Non-Conflicting)

These categories control independent `rcParams`, so they combine cleanly:

| Combination | Why It Works |
|---|---|
| Journal + Color | Journal sets sizes/fonts; color sets only `axes.prop_cycle` |
| Any + `grid` | `grid` only sets `axes.grid: True` and grid line width |
| Any + `no-latex` | `no-latex` only sets `text.usetex: False` |
| `scatter` + Color | `scatter` sets marker sizes; color sets the cycle |

```python
# All of these combine cleanly:
plt.style.use(['science', 'ieee', 'bright', 'grid'])
plt.style.use(['science', 'nature', 'muted'])
plt.style.use(['science', 'scatter', 'vibrant'])
```

### What Conflicts (Last One Wins)

| Conflicting Pair | Conflicting Parameter | Result |
|---|---|---|
| `ieee` + `nature` | `figure.figsize`, `font.family` | Last journal wins |
| `bright` + `vibrant` | `axes.prop_cycle` | Last color wins |
| `no-latex` + `latex-sans` | `text.usetex` | Last one wins |
| `notebook` + `ieee` | `figure.figsize`, `font.size` | Last one wins |

**Rule of thumb**: Never stack two styles from the same category.

```python
# ✗ BAD — ieee and nature both set figure.figsize and font.family
plt.style.use(['science', 'ieee', 'nature'])

# ✗ BAD — bright and muted both set axes.prop_cycle
plt.style.use(['science', 'bright', 'muted'])

# ✓ GOOD — one from each category
plt.style.use(['science', 'ieee', 'bright', 'grid'])
```

### CJK Language Styles: Must Include `no-latex`

CJK font styles set `font.family` to a CJK font that is incompatible with
LaTeX's default serif rendering. Always pair with `no-latex`:

```python
# ✓ Correct
plt.style.use(['science', 'no-latex', 'cjk-sc-font'])

# ✗ Will fail — LaTeX cannot render CJK fonts
plt.style.use(['science', 'cjk-sc-font'])
```

---

## Best Practices for Choosing Styles

### Decision Flowchart

```
Is this for a specific journal?
├─ Yes → use ['science', '<journal>']
│        e.g. ['science', 'ieee'] or ['science', 'nature']
└─ No
   ├─ Is this for a notebook or slides?
   │  └─ Yes → use ['science', 'no-latex', 'notebook']
   └─ No → use ['science'] as the base
         ├─ Need color-blind safe? → add 'bright' or 'vibrant'
         ├─ Need B/W safe?        → add 'high-contrast'
         ├─ Need grid?            → add 'grid'
         └─ No LaTeX?             → add 'no-latex'
```

### Recommended Combinations by Use Case

| Use Case | Recommended Combination |
|---|---|
| Generic paper figure | `['science']` |
| IEEE Transactions | `['science', 'ieee']` |
| Nature / Nature-family | `['science', 'nature']` |
| Jupyter notebook | `['science', 'no-latex', 'notebook']` |
| Conference slides | `['science', 'no-latex', 'notebook', 'vibrant']` |
| Color-blind safe paper | `['science', 'ieee', 'bright']` |
| Grayscale-safe figure | `['science', 'high-contrast']` |
| Chinese paper | `['science', 'no-latex', 'cjk-sc-font']` |
| Embed in LaTeX doc | `['science', 'pgf']` |
| Sans-serif LaTeX | `['science', 'latex-sans']` |
| Many data series (10+) | `['science', 'muted']` (10 colors) |
| Exact N colors | `['science', 'discrete-rainbow-N']` |

---

## Temporary Styles with `plt.style.context()`

Use `plt.style.context()` as a context manager to apply a style only within a
`with` block. The global `rcParams` are restored when the block exits.

### Basic Usage

```python
import matplotlib.pyplot as plt
import scienceplots

# Global style remains default matplotlib
with plt.style.context(['science', 'ieee']):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    fig.savefig('ieee_figure.pdf')
# Outside: rcParams are back to default
```

### Nesting Contexts

You can nest contexts to produce different-styled figures in sequence:

```python
with plt.style.context(['science', 'ieee', 'bright']):
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y1)
    fig1.savefig('figure1.pdf')

with plt.style.context(['science', 'nature', 'vibrant']):
    fig2, ax2 = plt.subplots()
    ax2.plot(x, y2)
    fig2.savefig('figure2.pdf')
```

### Combining with Manual rcParams Overrides

```python
with plt.style.context(['science', 'ieee']):
    plt.rcParams['lines.linewidth'] = 1.5  # Override within context
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.savefig('thicker_lines.pdf')
# linewidth is restored to default outside
```

### When to Use `context()` vs. `use()`

| Scenario | Use |
|---|---|
| All figures in a script share one style | `plt.style.use(...)` at the top |
| Different figures need different styles | `plt.style.context(...)` per figure |
| Interactive notebook, want to reset | `plt.style.context(...)` in cells |
| One-off styled figure in a larger app | `plt.style.context(...)` |

---

## Customizing rcParams on Top of SciencePlots

After applying a SciencePlots style, you can fine-tune any individual parameter:

### Method 1: Direct `rcParams` Dictionary Update

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

# Override specific parameters
plt.rcParams.update({
    'font.size': 10,            # Larger base font
    'lines.linewidth': 1.5,     # Thicker lines
    'figure.figsize': (4.0, 3.0),  # Custom size
    'legend.frameon': True,     # Add legend border
    'legend.edgecolor': '0.8',  # Light gray border
})
```

### Method 2: `matplotlib.rc()` Function

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'nature'])

# Group-based updates
mpl.rc('font', size=9, family='sans-serif')
mpl.rc('axes', labelsize=10, titlesize=11)
mpl.rc('lines', linewidth=1.2, markersize=4)
```

### Method 3: Per-Figure Overrides (No Global Side Effects)

```python
with plt.style.context(['science', 'ieee']):
    fig, ax = plt.subplots(figsize=(5, 3.5))  # Override figsize for this figure
    ax.plot(x, y, linewidth=2.0)              # Override linewidth for this line
    ax.set_xlabel('X', fontsize=10)            # Override label size
```

### Commonly Customized Parameters

| Parameter | Default (`science`) | Common Override | Why |
|---|---|---|---|
| `figure.figsize` | `(3.3, 2.5)` | `(6.5, 4.0)` | Full-width figure |
| `font.size` | `8` | `10`–`12` | Larger for slides |
| `lines.linewidth` | `1.0` | `1.5`–`2.0` | Thicker for visibility |
| `legend.frameon` | `False` | `True` | Add legend border |
| `axes.grid` | `False` | `True` | Add grid (or use `grid` style) |
| `savefig.dpi` | `600` | `300` | Smaller file for web |
| `savefig.bbox_inches` | — | `'tight'` | Remove whitespace |

---

## Creating Custom `.mplstyle` Files

You can create your own `.mplstyle` files that build on SciencePlots styles.
This is ideal when you want reusable custom settings across multiple projects.

### Step 1: Create the File

Create a file with the `.mplstyle` extension. The format is `key: value`, one
per line, with `#` for comments:

```ini
# my-paper.mplstyle
# Custom style for my research group's papers
# Designed to cascade on top of ['science', 'ieee']

# Slightly larger fonts for readability
font.size: 9
axes.labelsize: 9
legend.fontsize: 8

# Thicker lines
lines.linewidth: 1.3
axes.linewidth: 0.6

# Custom color cycle (our lab colors)
axes.prop_cycle: cycler('color', ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B'])

# Always save with tight bounding box
savefig.bbox_inches: tight
savefig.pad_inches: 0.05
```

### Step 2: Use the Custom Style

There are three ways to load a custom `.mplstyle` file:

```python
import matplotlib.pyplot as plt
import scienceplots

# Option A: Load by absolute/relative path
plt.style.use(['science', 'ieee', './my-paper.mplstyle'])

# Option B: Load via rc_file (does not support cascading)
import matplotlib
matplotlib.rc_file('./my-paper.mplstyle')

# Option C: Install into Matplotlib's style directory
# Copy to: <matplotlib_config>/stylelib/my-paper.mplstyle
# Then use by name:
plt.style.use(['science', 'ieee', 'my-paper'])
```

### Step 3: Find Matplotlib's Config Directory

```python
import matplotlib
print(matplotlib.get_configdir())
# e.g., ~/.config/matplotlib  (Linux)
#        ~/Library/Preferences/matplotlib  (macOS)
#        C:\Users\<user>\.matplotlib  (Windows)

# Style files go in: <configdir>/stylelib/
```

### Template: Research Group Style

```ini
# labstyle.mplstyle
# Cascades on top of ['science']

# Figure dimensions for double-column journal
figure.figsize: 6.5, 4.0

# Slightly larger fonts
font.size: 9
axes.labelsize: 10
axes.titlesize: 10
legend.fontsize: 8
xtick.labelsize: 8
ytick.labelsize: 8

# Lab color palette
axes.prop_cycle: cycler('color', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02'])

# Grid on by default
axes.grid: True
grid.alpha: 0.3
grid.linewidth: 0.4

# DPI
figure.dpi: 150
savefig.dpi: 600
savefig.bbox_inches: tight
```

---

## Consistent Figures Across a Paper

When writing a multi-figure paper, consistency is critical. Use a wrapper
function to enforce the same style, size, and save parameters on every figure.

### Wrapper Function Pattern

```python
import matplotlib.pyplot as plt
import scienceplots
from pathlib import Path

# === Configuration (edit once for the whole paper) ===
STYLE = ['science', 'ieee', 'bright']
FIG_DIR = Path('./figures')
FIG_DIR.mkdir(exist_ok=True)
SAVE_KWARGS = dict(dpi=600, bbox_inches='tight', pad_inches=0.02)

def paper_figure(name, figsize=None, nrows=1, ncols=1, **subplot_kw):
    """Create a figure with consistent style for the paper.

    Args:
        name: Filename stem (without extension). Will save as PDF and PNG.
        figsize: Override figure size. Defaults to style's figure.figsize.
        nrows, ncols: Subplot grid dimensions.
        **subplot_kw: Passed to plt.subplots().

    Returns:
        (fig, ax) tuple (ax may be an array for multi-panel figures).
    """
    plt.style.use(STYLE)
    kw = dict(**subplot_kw)
    if figsize:
        kw['figsize'] = figsize
    fig, ax = plt.subplots(nrows, ncols, **kw)
    return fig, ax

def save_figure(fig, name):
    """Save a figure in both PDF (for paper) and PNG (for draft preview)."""
    fig.savefig(FIG_DIR / f'{name}.pdf', **SAVE_KWARGS)
    fig.savefig(FIG_DIR / f'{name}.png', **SAVE_KWARGS)
    plt.close(fig)
    print(f'Saved: {name}.pdf, {name}.png')

# === Usage ===
fig, ax = paper_figure('fig1_convergence')
ax.plot(x, y, label='Method A')
ax.set_xlabel('Iteration')
ax.set_ylabel('Loss')
ax.legend()
save_figure(fig, 'fig1_convergence')

fig, axes = paper_figure('fig2_comparison', nrows=1, ncols=2)
axes[0].plot(x, y1)
axes[1].plot(x, y2)
save_figure(fig, 'fig2_comparison')
```

### Alternative: Context-Manager Wrapper

```python
from contextlib import contextmanager

@contextmanager
def paper_style():
    """Apply the paper's style as a context manager."""
    with plt.style.context(['science', 'ieee', 'bright']):
        yield

# Usage:
with paper_style():
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.savefig('figure.pdf', dpi=600, bbox_inches='tight')
```

---

## DPI and Figure Size Guidelines

### Figure Sizes by Output Target

| Target | Width | Height | `figure.figsize` | Notes |
|---|---|---|---|---|
| Single-column journal | 3.3 in (84 mm) | 2.5 in | `(3.3, 2.5)` | Default for `science` / `ieee` |
| Nature single-column | 3.5 in (89 mm) | 2.6 in | `(3.5, 2.625)` | Default for `nature` |
| Double-column journal | 6.5–7.0 in | 4.0–5.0 in | `(6.5, 4.0)` | Two-column width figure |
| Jupyter notebook | 8.0 in | 6.0 in | `(8, 6)` | Default for `notebook` |
| Presentation slide | 10 in | 6.0–7.0 in | `(10, 6)` | Fill 16:10 slide |
| Poster panel | 12–15 in | 8–10 in | `(12, 8)` | Large print |

### DPI by Output Target

| Target | Recommended DPI | `figure.dpi` | `savefig.dpi` | File Size Impact |
|---|---|---|---|---|
| Journal submission | 600 | `600` | `600` | Large PNGs, use PDF |
| Thesis / report | 300–600 | `150` | `300` | Moderate |
| Web / blog | 150 | `150` | `150` | Small |
| Jupyter notebook | 100–150 | `100` | `150` | Minimal |
| Slides / presentation | 150–200 | `150` | `200` | Moderate |

### Setting DPI

```python
# Via style
plt.style.use(['science', 'ieee'])  # DPI is 600

# Override for web output
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 150,
})

# Or per-save
fig.savefig('web_figure.png', dpi=150)
```

### File Format Recommendations

| Format | When to Use | DPI Matters? |
|---|---|---|
| **PDF** | Journal submission, LaTeX `\includegraphics` | No (vector) |
| **SVG** | Web, interactive reports | No (vector) |
| **PNG** | Notebooks, slides, drafts | Yes |
| **EPS** | Legacy journals | No (vector) |
| **TIFF** | Some biomedical journals | Yes (usually 300+) |
| **PGF** | Direct LaTeX integration | N/A (LaTeX renders) |

```python
# Save as PDF (best for papers)
fig.savefig('figure.pdf', bbox_inches='tight')

# Save as PNG (for slides, web)
fig.savefig('figure.png', dpi=200, bbox_inches='tight')

# Save as PGF (for LaTeX documents)
plt.style.use(['science', 'pgf'])
fig.savefig('figure.pgf')
```

### Golden Ratio for Aspect Ratios

A pleasing default is the golden ratio (≈ 1.618:1):

```python
width = 3.3  # single-column
height = width / 1.618
fig, ax = plt.subplots(figsize=(width, height))
```
