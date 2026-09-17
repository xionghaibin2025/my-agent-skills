# SciencePlots — Troubleshooting Guide

## Quick Diagnostic Script

Run this first to identify common issues:

```python
import sys
print(f"Python: {sys.version}")

import matplotlib
print(f"Matplotlib: {matplotlib.__version__}")

try:
    import scienceplots
    print(f"SciencePlots: {scienceplots.__version__}")
except ImportError:
    print("SciencePlots: NOT INSTALLED")

import shutil
print(f"LaTeX: {'Found' if shutil.which('latex') else 'NOT FOUND'}")

import matplotlib.pyplot as plt
sp_styles = [s for s in plt.style.available if 'science' in s or s in [
    'ieee', 'nature', 'bright', 'vibrant', 'muted', 'grid', 'no-latex', 'notebook'
]]
print(f"SciencePlots styles registered: {len(sp_styles)}")
print(f"Styles: {sp_styles}")
```

---

## Error: `OSError: 'science' is not a valid package style`

**Cause**: SciencePlots styles are not registered with Matplotlib. Since
SciencePlots v2.0.0, you **must** explicitly import the package before using
any of its styles.

**Fix**: Add `import scienceplots` before any `plt.style.use()` call:

```python
import matplotlib.pyplot as plt
import scienceplots  # ← This line is REQUIRED

plt.style.use('science')  # Now works
```

**Why this changed**: In older versions (< 2.0.0), SciencePlots installed its
`.mplstyle` files directly into Matplotlib's `stylelib` directory. Starting
with v2.0.0, styles are registered at import time via a `styles_discovery.py`
entry point. The explicit import triggers this registration.

**Still failing after import?** Check:
1. `scienceplots` is installed in the same Python environment as `matplotlib`.
2. Run `pip show SciencePlots` to confirm installation path.
3. Run `python -c "import scienceplots; print(scienceplots.__version__)"`.

---

## Error: LaTeX Not Found

### Symptom

```
RuntimeError: Failed to process string with tex because latex could not be found
```

or:

```
FileNotFoundError: [Errno 2] No such file or directory: 'latex'
```

### Cause

The `science` base style sets `text.usetex: True`, which requires a working
LaTeX installation on the system.

### Fix: Option A — Install LaTeX

| Platform | Install Command |
|---|---|
| **Ubuntu / Debian** | `sudo apt install texlive-latex-extra texlive-fonts-recommended dvipng cm-super` |
| **Fedora** | `sudo dnf install texlive-scheme-medium` |
| **macOS** | `brew install --cask mactex-no-gui` or install [MacTeX](https://www.tug.org/mactex/) |
| **Windows** | Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/) |
| **Conda** | `conda install -c conda-forge texlive-core` |

After installing, restart your Python kernel/session. Verify with:

```bash
latex --version
```

### Fix: Option B — Use `no-latex` Style (No Installation Required)

```python
plt.style.use(['science', 'no-latex'])
```

This disables LaTeX rendering (`text.usetex: False`) and uses Matplotlib's
built-in math text renderer instead. Figures will look slightly different from
LaTeX-rendered ones, but are perfectly usable.

---

## Error: CJK Font Not Found

### Symptom

```
findfont: Font family 'Noto Sans CJK SC' not found.
```

or characters appear as empty boxes (□□□).

### Cause

CJK font styles (`cjk-sc-font`, `cjk-tc-font`, `cjk-jp-font`, `cjk-kr-font`)
require the corresponding Noto Sans CJK fonts to be installed on the system.

### Fix

**Step 1**: Install the fonts.

```bash
# Option A: Use mplfonts (recommended, Python-native)
pip install mplfonts
mplfonts init  # Downloads and registers fonts with matplotlib

# Option B: Install system fonts manually
# Ubuntu/Debian:
sudo apt install fonts-noto-cjk

# macOS:
brew install font-noto-sans-cjk

# Windows:
# Download from https://fonts.google.com/noto → "Noto Sans CJK SC" (or TC/JP/KR)
# Double-click .otf files to install
```

**Step 2**: Clear Matplotlib's font cache.

```python
import matplotlib
from pathlib import Path

# Delete font cache
cache_dir = Path(matplotlib.get_cachedir())
for f in cache_dir.glob('fontlist-*.json'):
    f.unlink()
    print(f"Deleted: {f}")

print("Restart Python to rebuild the font cache.")
```

**Step 3**: Always use `no-latex` with CJK styles.

```python
# ✓ Correct
plt.style.use(['science', 'no-latex', 'cjk-sc-font'])

# ✗ Wrong — LaTeX cannot render CJK fonts with the default engine
plt.style.use(['science', 'cjk-sc-font'])
```

---

## Matplotlib Version Compatibility Issues

### Matplotlib 3.11+ Namespace Changes

Matplotlib 3.11 (released 2025) introduced changes to internal style discovery.
If you see warnings or errors after upgrading:

**Symptoms**:
- `DeprecationWarning` about style registration
- Styles not found despite `import scienceplots`

**Fix**: Upgrade SciencePlots to the latest version:

```bash
pip install --upgrade SciencePlots
```

SciencePlots ≥ 2.1.0 uses `matplotlib.style.core` entry points that are
compatible with Matplotlib 3.11+.

### Version Compatibility Table

| SciencePlots Version | Matplotlib Compatibility | Python |
|---|---|---|
| 2.1.x (latest) | 3.4 – 3.11+ | 3.8+ |
| 2.0.x | 3.4 – 3.10 | 3.7+ |
| 1.x (legacy) | 3.0 – 3.8 | 3.6+ |

### Checking Versions

```python
import matplotlib
import scienceplots

print(f"Matplotlib: {matplotlib.__version__}")
print(f"SciencePlots: {scienceplots.__version__}")
```

If using an older Matplotlib (< 3.4), upgrade:

```bash
pip install --upgrade matplotlib
```

---

## Figure Too Small / Too Large in Notebooks

### Symptom

Figures appear tiny in Jupyter notebooks, or text is unreadably small.

### Cause

The `science` base style sets `figure.figsize: (3.3, 2.5)` and `font.size: 8`,
which are optimized for journal column widths, not screen display.

### Fix: Use the `notebook` Style

```python
# For notebook display
plt.style.use(['science', 'no-latex', 'notebook'])
```

The `notebook` style overrides:

| Parameter | `science` default | `notebook` override |
|---|---|---|
| `figure.figsize` | `(3.3, 2.5)` | `(8, 6)` |
| `font.size` | `8` | `14` |
| `axes.labelsize` | `8` | `16` |
| `legend.fontsize` | `7` | `14` |
| `xtick.labelsize` | `7` | `12` |
| `ytick.labelsize` | `7` | `12` |
| `lines.linewidth` | `1.0` | `2.0` |

### Alternative: Manual Override

```python
plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    'figure.figsize': (8, 5),
    'font.size': 12,
})
```

### Jupyter-Specific: Use Retina Display

Add this to your notebook for crisp rendering on HiDPI screens:

```python
%config InlineBackend.figure_format = 'retina'
```

---

## Fonts Look Wrong in Saved PDF

### Symptom

- Fonts appear as outlines instead of text in PDF
- Text is not searchable/selectable in PDF
- PDF viewer shows substitute fonts

### Cause

Fonts may not be embedded in the PDF. This commonly happens with Type 3 fonts
or when the system font differs from what Matplotlib expects.

### Fix

**Option 1**: Force font embedding by using Type 42 (TrueType) fonts:

```python
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42   # TrueType
matplotlib.rcParams['ps.fonttype'] = 42    # TrueType for PS/EPS too
```

**Option 2**: Use the LaTeX-rendered path (default in SciencePlots):

```python
plt.style.use(['science', 'ieee'])
# text.usetex: True ensures LaTeX handles all fonts → always embedded
```

**Option 3**: Check embedded fonts in the PDF:

```bash
# Linux/macOS
pdffonts output.pdf

# Or use Python
pip install PyPDF2
python -c "
from PyPDF2 import PdfReader
r = PdfReader('output.pdf')
for page in r.pages:
    if '/Font' in page['/Resources']:
        for font in page['/Resources']['/Font'].values():
            print(font['/BaseFont'])
"
```

**Option 4**: Save as PGF for native LaTeX integration:

```python
plt.style.use(['science', 'pgf'])
fig.savefig('figure.pgf')
# Then in LaTeX: \input{figure.pgf}
```

---

## RuntimeError About Missing LaTeX Packages

### Symptom

```
RuntimeError: LaTeX Error: File `type1cm.sty' not found.
```

or similar missing `.sty` / `.cls` file errors.

### Cause

SciencePlots' LaTeX rendering requires certain LaTeX packages that may not be
included in minimal LaTeX installations.

### Fix

Install the missing packages:

```bash
# Ubuntu/Debian — install the comprehensive set
sudo apt install texlive-latex-extra texlive-fonts-recommended \
                 texlive-fonts-extra dvipng cm-super

# Fedora
sudo dnf install texlive-type1cm texlive-cm-super

# MiKTeX (Windows) — will auto-install on first use, or:
miktex-console  # Open MiKTeX Console → Packages → search and install

# TeX Live (manual)
tlmgr install type1cm cm-super dvipng
```

### Common Required LaTeX Packages

| Package | Needed For |
|---|---|
| `type1cm` | Scalable Computer Modern fonts |
| `cm-super` | Type 1 Computer Modern fonts |
| `dvipng` | Converting DVI to PNG |
| `amsmath` | Math symbols and environments |
| `sansmath` | Sans-serif math (`latex-sans` style) |
| `underscore` | Underscore characters in text mode |

### Workaround: Skip LaTeX Entirely

```python
plt.style.use(['science', 'no-latex'])
```

---

## Style Not Found After `pip install`

### Symptom

```python
import scienceplots
plt.style.use('science')
# OSError: 'science' is not a valid package style
```

Even though `import scienceplots` succeeds.

### Possible Causes and Fixes

**Cause 1**: Old version of SciencePlots.

```bash
pip install --upgrade SciencePlots
```

**Cause 2**: Multiple Python environments. The `scienceplots` import and
`matplotlib` import are from different environments.

```python
import scienceplots, matplotlib
print(scienceplots.__file__)   # Check where scienceplots is installed
print(matplotlib.__file__)     # Check where matplotlib is installed
# Both should be under the same site-packages
```

**Cause 3**: Cached `.pyc` files from an old installation.

```bash
pip uninstall SciencePlots
pip cache purge
pip install SciencePlots
```

**Cause 4**: Style registration failed silently.

```python
import matplotlib.pyplot as plt
import scienceplots

# Force-check what styles are available
print([s for s in plt.style.available if 'science' in s.lower()])
# Should print: ['science']

# Check the full list
print(sorted(plt.style.available))
```

---

## How to Check Available Styles

### List All Available Styles

```python
import matplotlib.pyplot as plt
import scienceplots

# All styles (matplotlib built-in + SciencePlots)
print(sorted(plt.style.available))
```

### Filter SciencePlots Styles Only

```python
# Known SciencePlots style names
SCIENCEPLOTS_STYLES = {
    'science', 'scatter',
    'ieee', 'nature',
    'bright', 'vibrant', 'muted', 'high-contrast', 'light',
    'high-vis', 'retro', 'std-colors',
    'cjk-sc-font', 'cjk-tc-font', 'cjk-jp-font', 'cjk-kr-font',
    'russian-font', 'turkish-font',
    'grid', 'no-latex', 'notebook', 'latex-sans', 'pgf',
}
# Plus discrete-rainbow-1 through discrete-rainbow-23
SCIENCEPLOTS_STYLES.update(f'discrete-rainbow-{i}' for i in range(1, 24))

available = set(plt.style.available)
registered = SCIENCEPLOTS_STYLES & available
missing = SCIENCEPLOTS_STYLES - available

print(f"Registered SciencePlots styles ({len(registered)}):")
for s in sorted(registered):
    print(f"  ✓ {s}")

if missing:
    print(f"\nMissing styles ({len(missing)}):")
    for s in sorted(missing):
        print(f"  ✗ {s}")
```

### Inspect a Style's Parameters

```python
# View what a specific style sets
print(plt.style.library['science'])
# Returns a dict of rcParams

# Compare two styles
import pprint
for key in ['ieee', 'nature']:
    print(f"\n--- {key} ---")
    pprint.pprint(dict(plt.style.library[key]))
```

---

## How to Reset to Default Matplotlib Style

### Full Reset

```python
import matplotlib.pyplot as plt

# Reset ALL rcParams to Matplotlib defaults
plt.rcdefaults()
```

### Reset to a Specific Style

```python
# Reset then apply a different style
plt.rcdefaults()
plt.style.use('ggplot')  # or any other style
```

### Reset Within a Context

```python
# Use default style for one figure, then go back
with plt.style.context('default'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.savefig('default_style.png')
```

### Reset Individual Parameters

```python
from matplotlib import rcParamsDefault

# Reset only font settings
plt.rcParams['font.size'] = rcParamsDefault['font.size']
plt.rcParams['font.family'] = rcParamsDefault['font.family']
```

---

## Common Warning Messages

### `MatplotlibDeprecationWarning` About Style Sheets

**Message**: Warning about style sheet entry format.

**Fix**: Usually safe to ignore. Upgrade SciencePlots and Matplotlib to latest:

```bash
pip install --upgrade SciencePlots matplotlib
```

### `UserWarning: Glyph ... missing from current font`

**Cause**: The current font does not support the character being rendered
(common with special symbols or non-Latin scripts).

**Fix**:
- For CJK text: use the appropriate CJK font style with `no-latex`
- For special symbols: ensure LaTeX is rendering the text, or switch fonts
- Verify font availability: `from matplotlib.font_manager import findSystemFonts; print(findSystemFonts())`

### `tight_layout: Falling back to Agg renderer`

**Cause**: Harmless warning when using non-Agg backends with `tight_layout`.

**Fix**: Safe to ignore, or use `bbox_inches='tight'` in `savefig()` instead of
`plt.tight_layout()`:

```python
fig.savefig('figure.pdf', bbox_inches='tight')
```
