# SciencePlots — API Reference

## Style Application API

### `plt.style.use(style)` — Permanent Style Application

Applies one or more styles to the **global** `rcParams` for the current Python
session. All subsequent figures will use this style until changed or reset.

```python
import matplotlib.pyplot as plt
import scienceplots

# Single style
plt.style.use('science')

# Multiple styles (cascading)
plt.style.use(['science', 'ieee', 'bright'])
```

**Signature**:

```python
matplotlib.pyplot.style.use(style: str | Path | list[str | Path]) -> None
```

**Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `style` | `str`, `Path`, or `list` | Style name, path to `.mplstyle` file, or list of either |

**Behavior**:
- When given a list, styles are applied left-to-right.
- Later styles override earlier ones for conflicting `rcParams`.
- Non-conflicting parameters accumulate.
- Changes are **permanent** for the session (unlike `context()`).

**Valid `style` values**:
- A registered style name: `'science'`, `'ieee'`, `'bright'`, etc.
- A built-in Matplotlib style: `'ggplot'`, `'seaborn-v0_8'`, etc.
- A path to a `.mplstyle` file: `'./my-style.mplstyle'` or `Path('./custom.mplstyle')`
- The literal string `'default'` to reset to Matplotlib defaults.

```python
# Reset to defaults, then apply custom style
plt.style.use('default')
plt.style.use(['science', 'ieee'])

# Load from file
plt.style.use(['science', './lab-colors.mplstyle'])
```

---

### `plt.style.use([style1, style2, ...])` — Cascading Multiple Styles

When a list of styles is passed, they are applied sequentially. This is the
primary mechanism for building up a SciencePlots configuration.

```python
# Cascade order: base → journal → color → misc
plt.style.use(['science', 'ieee', 'vibrant', 'grid'])
```

**How cascading works internally**:

```python
# Pseudocode of what plt.style.use(['A', 'B', 'C']) does:
plt.rcParams.update(load_style('A'))  # Apply A
plt.rcParams.update(load_style('B'))  # B overrides A's conflicts
plt.rcParams.update(load_style('C'))  # C overrides A+B's conflicts
```

**Key rules**:
1. `science` should always be first (sets the base).
2. Journal styles second (override size/font).
3. Color styles third (override only color cycle).
4. Misc styles last (`grid`, `no-latex`, `notebook`).

**Conflict resolution**: The **last** style in the list wins for any shared
`rcParam` key.

---

### `plt.style.context(style)` — Temporary Style Context Manager

Applies a style temporarily within a `with` block. When the block exits,
`rcParams` are restored to their previous values.

```python
import matplotlib.pyplot as plt
import scienceplots

# Temporarily use SciencePlots styles
with plt.style.context(['science', 'ieee', 'bright']):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    fig.savefig('ieee_figure.pdf')

# rcParams are now back to what they were before the `with` block
```

**Signature**:

```python
matplotlib.pyplot.style.context(
    style: str | Path | list[str | Path],
    after_reset: bool = False
) -> contextlib.AbstractContextManager
```

**Parameters**:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `style` | `str`, `Path`, or `list` | (required) | Style(s) to apply |
| `after_reset` | `bool` | `False` | If `True`, reset to defaults first, then apply style |

**Examples**:

```python
# Clean application (reset defaults first, then apply)
with plt.style.context(['science', 'nature'], after_reset=True):
    fig, ax = plt.subplots()
    # ...

# Nest multiple contexts for different figures
with plt.style.context(['science', 'ieee']):
    make_ieee_figure()

with plt.style.context(['science', 'nature']):
    make_nature_figure()
```

---

### `plt.style.available` — List All Available Styles

A list of all registered style names (both built-in and from installed packages
like SciencePlots).

```python
import matplotlib.pyplot as plt
import scienceplots

# List all styles
print(plt.style.available)

# Filter for SciencePlots styles
for s in sorted(plt.style.available):
    print(s)
```

**Type**: `list[str]`

**Example output** (subset):

```
['Solarize_Light2', 'bmh', 'bright', 'classic', 'cjk-sc-font', ...,
 'dark_background', 'discrete-rainbow-1', ..., 'grid', 'high-contrast',
 'high-vis', 'ieee', 'light', 'muted', 'nature', 'no-latex', 'notebook',
 'pgf', 'retro', 'scatter', 'science', 'std-colors', 'vibrant', ...]
```

**Note**: SciencePlots styles only appear after `import scienceplots`.

---

### `plt.style.library` — Dict of All Style Definitions

A dictionary mapping style names to their `rcParams` dictionaries.

```python
import matplotlib.pyplot as plt
import scienceplots

# Get the rcParams for a specific style
science_params = plt.style.library['science']
print(science_params)

# Compare two styles
ieee_params = plt.style.library['ieee']
for key in ieee_params:
    print(f"  {key}: {ieee_params[key]}")
```

**Type**: `dict[str, dict[str, Any]]`

**Usage**: Useful for inspecting what a style actually sets, or for
programmatically building custom style combinations.

```python
# Merge two styles manually
import copy
merged = copy.deepcopy(plt.style.library['science'])
merged.update(plt.style.library['ieee'])
plt.rcParams.update(merged)
```

---

## rcParams API

### `plt.rcParams` — Read / Modify Individual Parameters

The global `rcParams` object is a dictionary-like object that controls all
Matplotlib defaults.

```python
import matplotlib.pyplot as plt

# Read a parameter
print(plt.rcParams['figure.figsize'])    # e.g., [3.3, 2.5]
print(plt.rcParams['font.size'])         # e.g., 8.0
print(plt.rcParams['text.usetex'])       # e.g., True

# Modify a single parameter
plt.rcParams['lines.linewidth'] = 1.5

# Modify multiple parameters
plt.rcParams.update({
    'figure.figsize': (6.5, 4.0),
    'font.size': 10,
    'axes.grid': True,
})
```

**Type**: `matplotlib.RcParams` (dict-like, with validation)

**Key behavior**:
- Validates values on assignment (raises `ValueError` for invalid values).
- Changes affect all subsequent plots.
- Use `plt.rcdefaults()` to reset.

---

### `matplotlib.rc()` — Programmatic Group-Based Updates

Updates `rcParams` for a specific group (e.g., `font`, `axes`, `lines`).

```python
import matplotlib as mpl

# Update font settings
mpl.rc('font', size=10, family='sans-serif', weight='normal')

# Update axes settings
mpl.rc('axes', labelsize=12, titlesize=14, grid=True)

# Update line settings
mpl.rc('lines', linewidth=1.5, markersize=5)

# Update tick settings
mpl.rc('xtick', labelsize=10, direction='out')
mpl.rc('ytick', labelsize=10, direction='out')

# Update legend settings
mpl.rc('legend', fontsize=9, frameon=True, edgecolor='0.8')
```

**Signature**:

```python
matplotlib.rc(group: str, **kwargs) -> None
```

**Parameters**:

| Parameter | Type | Description |
|---|---|---|
| `group` | `str` | rcParams group name (e.g., `'font'`, `'axes'`, `'lines'`) |
| `**kwargs` | | Key-value pairs for the group's parameters |

**Note**: `mpl.rc('font', size=10)` is equivalent to `plt.rcParams['font.size'] = 10`.

---

### `matplotlib.rc_file()` — Load Custom `.mplstyle` Files

Loads `rcParams` from a `.mplstyle` file.

```python
import matplotlib as mpl

# Load from a file path
mpl.rc_file('./my-custom-style.mplstyle')

# With use_default_template=True, defaults are applied first
mpl.rc_file('./my-custom-style.mplstyle', use_default_template=True)
```

**Signature**:

```python
matplotlib.rc_file(fname: str | Path, *, use_default_template: bool = True) -> None
```

**Parameters**:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `fname` | `str` or `Path` | (required) | Path to `.mplstyle` file |
| `use_default_template` | `bool` | `True` | Reset to defaults before loading |

**Note**: Unlike `plt.style.use()`, this does **not** support cascading
multiple files. To cascade, use `plt.style.use([...])` instead:

```python
# ✓ Cascading with plt.style.use
plt.style.use(['science', './my-overrides.mplstyle'])

# ✗ rc_file does not cascade — it replaces
mpl.rc_file('./my-overrides.mplstyle')
```

---

### `plt.rcdefaults()` — Reset to Defaults

Resets all `rcParams` to Matplotlib's built-in defaults. This removes all
effects of any previously applied styles.

```python
import matplotlib.pyplot as plt

# Apply a style
plt.style.use(['science', 'ieee'])

# ... create figures ...

# Reset everything
plt.rcdefaults()

# Now rcParams are back to Matplotlib's defaults
print(plt.rcParams['figure.figsize'])  # [6.4, 4.8]
print(plt.rcParams['text.usetex'])     # False
```

**Signature**:

```python
matplotlib.pyplot.rcdefaults() -> None
```

**Alternative**: Use `plt.style.use('default')` for the same effect.

---

## Key rcParams Categories

### `figure` — Figure-Level Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `figure.figsize` | `(float, float)` | `(3.3, 2.5)` | Figure width, height in inches |
| `figure.dpi` | `float` | `600` | Screen resolution |
| `figure.facecolor` | `color` | `'white'` | Figure background color |
| `figure.edgecolor` | `color` | `'white'` | Figure border color |
| `figure.autolayout` | `bool` | `False` | Auto-call `tight_layout` |
| `figure.constrained_layout.use` | `bool` | `False` | Use constrained layout |

### `font` — Font Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `font.family` | `str` | `'serif'` | Font family: `serif`, `sans-serif`, `monospace` |
| `font.size` | `float` | `8` | Base font size in points |
| `font.weight` | `str` | `'normal'` | Font weight: `normal`, `bold` |
| `font.serif` | `list[str]` | (system default) | Serif font names |
| `font.sans-serif` | `list[str]` | (system default) | Sans-serif font names |

### `axes` — Axes Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `axes.labelsize` | `float` or `str` | `8` | Axis label font size |
| `axes.titlesize` | `float` or `str` | `8` | Axes title font size |
| `axes.linewidth` | `float` | `0.5` | Border line width |
| `axes.grid` | `bool` | `False` | Show grid (`True` with `grid` style) |
| `axes.prop_cycle` | `cycler` | 7-color cycle | Color cycle for plot lines |
| `axes.facecolor` | `color` | `'white'` | Axes background color |
| `axes.edgecolor` | `color` | `'black'` | Axes border color |
| `axes.labelpad` | `float` | `4.0` | Padding between label and axis |

### `lines` — Line Plot Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `lines.linewidth` | `float` | `1.0` | Line width in points |
| `lines.markersize` | `float` | `3` | Marker size in points |
| `lines.markeredgewidth` | `float` | `0.5` | Marker edge width |
| `lines.linestyle` | `str` | `'-'` | Default line style |

### `grid` — Grid Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `grid.linewidth` | `float` | `0.5` | Grid line width |
| `grid.alpha` | `float` | `1.0` | Grid line transparency |
| `grid.color` | `color` | `'#b0b0b0'` | Grid line color |
| `grid.linestyle` | `str` | `'-'` | Grid line style |

### `legend` — Legend Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `legend.fontsize` | `float` or `str` | `7` | Legend text size |
| `legend.frameon` | `bool` | `False` | Draw legend border |
| `legend.loc` | `str` | `'best'` | Legend location |
| `legend.numpoints` | `int` | `1` | Points in legend handle |
| `legend.scatterpoints` | `int` | `3` | Scatter points in legend |
| `legend.edgecolor` | `color` | `'0.8'` | Legend border color |
| `legend.fancybox` | `bool` | `True` | Round legend corners |

### `xtick` / `ytick` — Tick Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `xtick.direction` | `str` | `'in'` | Tick direction: `in`, `out`, `inout` |
| `xtick.major.size` | `float` | `3` | Major tick length |
| `xtick.minor.size` | `float` | `1.5` | Minor tick length |
| `xtick.major.width` | `float` | `0.5` | Major tick width |
| `xtick.labelsize` | `float` or `str` | `7` | Tick label font size |
| `xtick.minor.visible` | `bool` | `True` | Show minor ticks |
| `ytick.direction` | `str` | `'in'` | Same as xtick |
| `ytick.major.size` | `float` | `3` | Same as xtick |
| `ytick.minor.visible` | `bool` | `True` | Same as xtick |

### `savefig` — Save Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `savefig.dpi` | `float` | `600` | Resolution when saving |
| `savefig.format` | `str` | `'png'` | Default save format |
| `savefig.bbox_inches` | `str` or `None` | `None` | `'tight'` to remove whitespace |
| `savefig.pad_inches` | `float` | `0.1` | Padding when `bbox_inches='tight'` |
| `savefig.facecolor` | `color` | `'auto'` | Saved figure background |
| `savefig.transparent` | `bool` | `False` | Transparent background |

### `text` — Text Rendering Settings

| Parameter | Type | `science` Default | Description |
|---|---|---|---|
| `text.usetex` | `bool` | `True` | Use LaTeX for text rendering |
| `text.latex.preamble` | `str` | `''` | Extra LaTeX preamble commands |
| `text.color` | `color` | `'black'` | Default text color |

---

## How SciencePlots Registers Styles

### Registration Mechanism

SciencePlots uses Matplotlib's style discovery system to register its bundled
`.mplstyle` files. The process works as follows:

### 1. Package Entry Point (`__init__.py`)

When you `import scienceplots`, the package's `__init__.py` executes and
triggers style registration:

```python
# scienceplots/__init__.py (simplified)
import os
from pathlib import Path

# Find all .mplstyle files in the package's styles/ directory
_stylesheets_dir = Path(__file__).parent / 'styles'

def _register_styles():
    """Register all bundled .mplstyle files with matplotlib."""
    import matplotlib.pyplot as plt

    # Walk the styles directory tree
    for dirpath, _, filenames in os.walk(_stylesheets_dir):
        for filename in filenames:
            if filename.endswith('.mplstyle'):
                style_path = Path(dirpath) / filename
                style_name = filename[:-len('.mplstyle')]
                # Read and parse the style file
                plt.style.library[style_name] = _read_style(style_path)

    # Update the available styles list
    plt.style.reload_library()

_register_styles()
```

### 2. Style Discovery (`styles_discovery.py`)

In SciencePlots ≥ 2.0.0, styles are registered via Python's
`importlib.metadata` entry points. The `setup.py` or `pyproject.toml` declares:

```toml
# pyproject.toml
[project.entry-points."matplotlib.style"]
scienceplots = "scienceplots.styles_discovery:discover_styles"
```

This tells Matplotlib to call `discover_styles()` when loading styles,
returning the paths to all bundled `.mplstyle` files.

### 3. Directory Structure

```
scienceplots/
├── __init__.py
├── styles_discovery.py
└── styles/
    ├── science.mplstyle          # Base style
    ├── scatter.mplstyle          # Scatter optimizations
    ├── journals/
    │   ├── ieee.mplstyle
    │   └── nature.mplstyle
    ├── color/
    │   ├── bright.mplstyle
    │   ├── vibrant.mplstyle
    │   ├── muted.mplstyle
    │   ├── high-contrast.mplstyle
    │   ├── light.mplstyle
    │   ├── high-vis.mplstyle
    │   ├── retro.mplstyle
    │   ├── std-colors.mplstyle
    │   └── discrete-rainbow-*.mplstyle  (1–23)
    ├── languages/
    │   ├── cjk-sc-font.mplstyle
    │   ├── cjk-tc-font.mplstyle
    │   ├── cjk-jp-font.mplstyle
    │   ├── cjk-kr-font.mplstyle
    │   ├── russian-font.mplstyle
    │   └── turkish-font.mplstyle
    └── misc/
        ├── grid.mplstyle
        ├── no-latex.mplstyle
        ├── notebook.mplstyle
        ├── latex-sans.mplstyle
        └── pgf.mplstyle
```

### 4. Why `import scienceplots` Is Required

Before v2.0.0, SciencePlots copied `.mplstyle` files directly into
Matplotlib's `stylelib/` directory during `pip install`. This was fragile
(broke on Matplotlib upgrades, required write access to site-packages).

Since v2.0.0, styles are bundled **inside** the `scienceplots` package and
registered at import time. This means:

- `pip install SciencePlots` → installs the package (styles are not yet visible)
- `import scienceplots` → registers styles with `plt.style.library`
- `plt.style.use('science')` → now works

If you skip the import, Matplotlib has no knowledge of SciencePlots' styles.

### Verifying Registration

```python
import matplotlib.pyplot as plt

# Before import — 'science' is NOT available
print('science' in plt.style.available)  # False

import scienceplots

# After import — 'science' IS available
print('science' in plt.style.available)  # True

# Full list of registered styles
for name, params in sorted(plt.style.library.items()):
    n_params = len(params)
    print(f"  {name:25s} ({n_params} params)")
```

---

## Quick Reference Table

| API | Purpose | Scope | Reversible? |
|---|---|---|---|
| `plt.style.use(style)` | Apply style globally | Session-wide | `plt.rcdefaults()` |
| `plt.style.use([...])` | Cascade multiple styles | Session-wide | `plt.rcdefaults()` |
| `plt.style.context(style)` | Apply style temporarily | `with` block | Automatic |
| `plt.style.available` | List all style names | Read-only | — |
| `plt.style.library` | Dict of style definitions | Read-only | — |
| `plt.rcParams[key] = val` | Set one parameter | Session-wide | Manual |
| `plt.rcParams.update({...})` | Set multiple parameters | Session-wide | Manual |
| `mpl.rc(group, **kw)` | Group-based parameter update | Session-wide | Manual |
| `mpl.rc_file(path)` | Load params from file | Session-wide | Manual |
| `plt.rcdefaults()` | Reset to Matplotlib defaults | Session-wide | — |
| `plt.style.use('default')` | Same as `rcdefaults()` | Session-wide | — |
