# Environment Setup & Installation Check

## Installation

SciencePlots must be installed before use. Run **one** of:

```bash
# From PyPI (recommended)
pip install SciencePlots

# From conda-forge
conda install -c conda-forge scienceplots

# Latest dev version from GitHub
pip install git+https://github.com/garrettj403/SciencePlots
```

## Critical Import Rule

Since **SciencePlots v2.0.0**, you **must** add `import scienceplots` before
setting styles. This registers the bundled stylesheets with Matplotlib.

```python
import matplotlib.pyplot as plt
import scienceplots  # REQUIRED — registers styles with matplotlib

plt.style.use('science')
```

Without `import scienceplots`, Matplotlib will raise:
`OSError: 'science' is not a valid package style`

## LaTeX Dependency

The default `science` style uses LaTeX for text rendering (`text.usetex: True`).

- **If LaTeX is installed**: styles work out of the box with publication-quality
  math typesetting.
- **If LaTeX is NOT installed**: add `'no-latex'` to your style list:
  ```python
  plt.style.use(['science', 'no-latex'])
  ```

### Installing LaTeX

| Platform | Command |
|---|---|
| Ubuntu/Debian | `sudo apt install texlive-latex-extra texlive-fonts-recommended dvipng cm-super` |
| Fedora | `sudo dnf install texlive-scheme-medium` |
| macOS | Install [MacTeX](https://www.tug.org/mactex/) or `brew install --cask mactex-no-gui` |
| Windows | Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/) |
| Conda | `conda install -c conda-forge texlive-core` |

## CJK Font Support

For Chinese, Japanese, or Korean text, install additional fonts:

```bash
# Install the mplfonts package (recommended replacement for deprecated CJK styles)
pip install mplfonts

# Or install system fonts manually:
# - Simplified Chinese: Noto Sans CJK SC
# - Traditional Chinese: Noto Sans CJK TC
# - Japanese: Noto Sans CJK JP
# - Korean: Noto Sans CJK KR
```

When using CJK styles, always combine with `no-latex`:
```python
plt.style.use(['science', 'no-latex', 'cjk-sc-font'])
```

## Quick Verification Script

```python
import matplotlib.pyplot as plt

try:
    import scienceplots
    print("✓ SciencePlots is installed")
except ImportError:
    print("✗ SciencePlots is NOT installed — run: pip install SciencePlots")

# Check available SciencePlots styles
sp_styles = [s for s in plt.style.available if not s.startswith('_')]
print(f"Available styles: {len(sp_styles)}")

# Check LaTeX
import shutil
if shutil.which('latex'):
    print("✓ LaTeX is available")
else:
    print("✗ LaTeX not found — use 'no-latex' style")
```
