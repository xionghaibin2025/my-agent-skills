# SciencePlots Quick-Start Examples

Five complete, fully runnable examples. Each generates its own sample data—
just copy, paste, and execute.

> **Prerequisites:** `pip install SciencePlots matplotlib numpy`
> Add `'no-latex'` to the style list if LaTeX is not installed.

---

## Example 1 — Basic Sine Wave (`science` Style)

A minimal single-panel plot showing the default `science` style.

```python
"""Example 1: Basic sine wave with the 'science' style."""

import matplotlib.pyplot as plt
import scienceplots
import numpy as np

# --- Style ---
plt.style.use(['science'])
# plt.style.use(['science', 'no-latex'])   # uncomment if no LaTeX

# --- Data ---
x = np.linspace(0, 2 * np.pi, 300)
y_sin = np.sin(x)
y_cos = np.cos(x)

# --- Plot ---
fig, ax = plt.subplots(figsize=(3.5, 2.625))  # single-column width

ax.plot(x, y_sin, label=r'$\sin(x)$')
ax.plot(x, y_cos, label=r'$\cos(x)$', linestyle='--')

ax.set_xlabel(r'Angle $\theta$ (rad)')
ax.set_ylabel(r'Amplitude')
ax.set_title('Trigonometric Functions')
ax.legend(loc='lower left')

ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.3, 1.3)

# --- Save ---
fig.savefig('example1_sine.pdf', dpi=300, bbox_inches='tight')
fig.savefig('example1_sine.png', dpi=600, bbox_inches='tight')
plt.show()
print('✓ Saved example1_sine.pdf / .png')
```

---

## Example 2 — IEEE-Formatted Comparison of Two Datasets

Generates two synthetic datasets (e.g., simulation vs. experiment) and
plots them side-by-side in IEEE double-column format.

```python
"""Example 2: IEEE-formatted comparison of two datasets."""

import matplotlib.pyplot as plt
import scienceplots
import numpy as np

# --- Style: science + ieee ---
plt.style.use(['science', 'ieee'])
# plt.style.use(['science', 'ieee', 'no-latex'])  # without LaTeX

# --- Synthetic data ---
rng = np.random.default_rng(2026)
freq = np.linspace(1, 100, 50)                     # frequency (Hz)
gain_sim = 20 * np.log10(1 / np.sqrt(1 + (freq / 30)**2))  # 1st-order LPF
gain_exp = gain_sim + rng.normal(0, 0.8, size=freq.shape)   # noisy measurement

# --- Plot ---
fig, ax = plt.subplots(figsize=(3.3, 2.5))  # IEEE single-column ≈ 3.3 in

ax.plot(freq, gain_sim, label='Simulation', linewidth=1.0)
ax.plot(freq, gain_exp, 'o', label='Experiment',
        markersize=2.5, markerfacecolor='none', markeredgewidth=0.6)

ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Gain (dB)')
ax.set_title('Low-Pass Filter Response')
ax.legend()

# Log scale on x-axis is common for Bode plots
ax.set_xscale('log')
ax.set_xlim(1, 100)

# --- Save ---
fig.savefig('example2_ieee.pdf', dpi=300, bbox_inches='tight')
fig.savefig('example2_ieee.png', dpi=600, bbox_inches='tight')
plt.show()
print('✓ Saved example2_ieee.pdf / .png')
```

---

## Example 3 — Nature-Style Multi-Panel Figure

A 1×3 panel figure styled for *Nature*-family journals, with panel labels
(a), (b), (c) and shared data.

```python
"""Example 3: Nature-style multi-panel figure."""

import matplotlib.pyplot as plt
import scienceplots
import numpy as np

# --- Style: science + nature ---
plt.style.use(['science', 'nature'])
# plt.style.use(['science', 'nature', 'no-latex'])  # without LaTeX

# --- Synthetic data ---
rng = np.random.default_rng(42)
time = np.linspace(0, 10, 200)

# Panel (a): population growth curves
pop_a = 100 * (1 - np.exp(-0.5 * time)) + rng.normal(0, 2, 200)
pop_b = 80 * (1 - np.exp(-0.3 * time)) + rng.normal(0, 2, 200)

# Panel (b): bar chart of final populations
final_pops = [pop_a[-20:].mean(), pop_b[-20:].mean()]
final_errs = [pop_a[-20:].std(), pop_b[-20:].std()]

# Panel (c): scatter of growth rate vs. final size
n_points = 30
growth_rates = rng.uniform(0.1, 0.8, n_points)
final_sizes = 50 + 100 * growth_rates + rng.normal(0, 5, n_points)

# --- Figure ---
fig, axes = plt.subplots(1, 3, figsize=(7, 2.2), constrained_layout=True)

# (a) Line plot
ax = axes[0]
ax.plot(time, pop_a, label='Species A')
ax.plot(time, pop_b, label='Species B')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Population')
ax.legend(fontsize=5)

# (b) Bar chart
ax = axes[1]
colors = ['#0C5DA5', '#FF2C00']
ax.bar(['Species A', 'Species B'], final_pops, yerr=final_errs,
       color=colors, capsize=3, width=0.5)
ax.set_ylabel('Final Population')

# (c) Scatter
ax = axes[2]
ax.scatter(growth_rates, final_sizes, s=15, edgecolors='k', linewidths=0.3)
# Linear fit
z = np.polyfit(growth_rates, final_sizes, 1)
p = np.poly1d(z)
x_fit = np.linspace(growth_rates.min(), growth_rates.max(), 50)
ax.plot(x_fit, p(x_fit), 'r--', linewidth=0.8, label=f'Fit: $y={z[0]:.0f}x+{z[1]:.0f}$')
ax.set_xlabel('Growth Rate')
ax.set_ylabel('Final Size')
ax.legend(fontsize=5)

# Panel labels
for idx, ax in enumerate(axes):
    label = chr(ord('a') + idx)
    ax.text(-0.2, 1.08, f'({label})', transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='bottom', ha='right')

# --- Save ---
fig.savefig('example3_nature.pdf', dpi=300, bbox_inches='tight')
fig.savefig('example3_nature.png', dpi=600, bbox_inches='tight')
plt.show()
print('✓ Saved example3_nature.pdf / .png')
```

---

## Example 4 — Notebook-Friendly Plot (Bright Colors + Grid)

Interactive-style plot optimized for Jupyter notebooks with the `bright`
color cycle and `grid` background.

```python
"""Example 4: Notebook-friendly plot with bright colors and grid."""

import matplotlib.pyplot as plt
import scienceplots
import numpy as np

# --- Style: science + bright + grid ---
# 'bright' provides a vivid, high-contrast color cycle
# 'grid' adds background grid lines for readability
plt.style.use(['science', 'bright', 'grid'])
# plt.style.use(['science', 'bright', 'grid', 'no-latex'])  # without LaTeX

# --- Synthetic data: multiple time series ---
rng = np.random.default_rng(7)
t = np.linspace(0, 5, 300)

fig, ax = plt.subplots(figsize=(5, 3.5))

for i, (amp, freq, name) in enumerate([
    (1.0, 1.0, 'Channel 1'),
    (0.8, 1.5, 'Channel 2'),
    (1.2, 0.7, 'Channel 3'),
    (0.6, 2.0, 'Channel 4'),
    (0.9, 1.2, 'Channel 5'),
]):
    signal = amp * np.sin(2 * np.pi * freq * t) + 0.1 * rng.normal(size=len(t))
    ax.plot(t, signal, label=name, linewidth=1.0)

ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (mV)')
ax.set_title('Multi-Channel Signal Recording')
ax.legend(ncol=3, loc='upper center', fontsize=7,
          bbox_to_anchor=(0.5, -0.18))

# --- Save ---
fig.savefig('example4_notebook.pdf', dpi=300, bbox_inches='tight')
fig.savefig('example4_notebook.png', dpi=300, bbox_inches='tight')
plt.show()
print('✓ Saved example4_notebook.pdf / .png')
```

---

## Example 5 — Chinese-Labeled Plot (no-latex + CJK Font)

Uses `no-latex` (since LaTeX is not needed) and CJK-compatible font
settings to render Chinese axis labels and titles.

```python
"""Example 5: Chinese-labeled plot with no-latex and CJK font support."""

import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import matplotlib

# --- Style: science + no-latex + cjk-sc-font ---
# 'no-latex'      — avoids LaTeX rendering (LaTeX doesn't handle CJK easily)
# 'cjk-sc-font'   — configures a Simplified Chinese font (e.g., SimHei / Noto Sans CJK SC)
# If 'cjk-sc-font' is unavailable, manually set font below.
try:
    plt.style.use(['science', 'no-latex', 'cjk-sc-font'])
except OSError:
    # Fallback: apply 'science' + 'no-latex' and configure font manually
    plt.style.use(['science', 'no-latex'])
    # Use a CJK font available on your system:
    #   Windows: 'SimHei', 'Microsoft YaHei'
    #   macOS:   'PingFang SC', 'Heiti SC'
    #   Linux:   'Noto Sans CJK SC', 'WenQuanYi Micro Hei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei',
                                               'Noto Sans CJK SC', 'PingFang SC']
    matplotlib.rcParams['axes.unicode_minus'] = False  # fix minus sign display

# --- 数据 (Data) ---
rng = np.random.default_rng(2026)
cities = ['北京', '上海', '广州', '深圳', '成都', '杭州']
temperature = [26.3, 28.1, 30.5, 29.8, 25.2, 27.6]            # ℃
humidity    = [55, 72, 80, 78, 65, 70]                          # %
rainfall   = [120 + rng.integers(-20, 20) for _ in cities]      # mm

# --- 图表 (Plot) ---
fig, axes = plt.subplots(1, 2, figsize=(7, 2.8), constrained_layout=True)

# 左图：柱状图 (Left: Bar chart)
ax = axes[0]
x_pos = np.arange(len(cities))
bars = ax.bar(x_pos, temperature, color='#0C5DA5', width=0.6)
ax.set_xticks(x_pos)
ax.set_xticklabels(cities, fontsize=7)
ax.set_xlabel('城市')          # City
ax.set_ylabel('平均温度 (℃)')  # Average Temperature
ax.set_title('中国主要城市 7 月平均气温')  # Average July Temperature in Major Chinese Cities
ax.set_ylim(20, 35)

# 在柱顶显示数值 (show values on top of bars)
for bar, val in zip(bars, temperature):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f'{val}', ha='center', va='bottom', fontsize=6)

# 右图：折线 + 散点 (Right: Line + Scatter)
ax = axes[1]
ax.plot(cities, rainfall, 'o-', color='#FF2C00', markersize=4, label='降水量 (mm)')
ax.set_xlabel('城市')
ax.set_ylabel('降水量 (mm)')   # Rainfall
ax.set_title('中国主要城市 7 月降水量')
ax.legend(fontsize=6)

# Rotate x-tick labels if they overlap
plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=7)

# --- 保存 (Save) ---
fig.savefig('example5_chinese.pdf', dpi=300, bbox_inches='tight')
fig.savefig('example5_chinese.png', dpi=600, bbox_inches='tight')
plt.show()
print('✓ 已保存 example5_chinese.pdf / .png')
```

> **Tip (提示):** Other CJK font styles available in SciencePlots:
>
> | Style Name       | Language               |
> |------------------|------------------------|
> | `cjk-sc-font`   | Simplified Chinese 简体 |
> | `cjk-tc-font`   | Traditional Chinese 繁體|
> | `cjk-jp-font`   | Japanese 日本語         |
> | `cjk-kr-font`   | Korean 한국어           |

---

## Running All Examples

Save each block to its own `.py` file or run all at once:

```bash
# Run individually
python example1_sine.py
python example2_ieee.py
python example3_nature.py
python example4_notebook.py
python example5_chinese.py
```

All output figures are saved as both **PDF** (vector) and **PNG** (raster)
in the current working directory.
