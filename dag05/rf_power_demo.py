from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Presentation settings: 2400 x 1350 pixel PNGs.
FONT_SIZE = 22
DPI = 200
OUTPUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    'font.size': FONT_SIZE,
    'axes.labelsize': FONT_SIZE + 2,
    'axes.titlesize': FONT_SIZE + 6,
    'xtick.labelsize': FONT_SIZE - 2,
    'ytick.labelsize': FONT_SIZE - 2,
    'axes.linewidth': 1.2,
    'font.family': 'DejaVu Sans',
})

# Synthetic data approximating the reference images, not digitized data.
# Exponentially distributed power approximates a noise-like RF spectrum.
rng = np.random.default_rng(42)
frequency_GHz = np.linspace(0, 1, 2001)
power_mW = np.maximum(rng.exponential(scale=0.7, size=2001), 1e-3)

# Two narrow peaks: 1000 mW = 30 dBm; 10 mW = 10 dBm.
for frequency, peak_mW in [(0.15, 1000.0), (0.30, 10.0)]:
    index = np.argmin(np.abs(frequency_GHz - frequency))
    power_mW[index] = peak_mW

# dBm is power relative to 1 mW. Both plots use exactly the same data.
power_dBm = 10 * np.log10(power_mW / 1.0)

plots = [
    (power_mW, 'RF uteffekt – linjär skala', 'Effekt (mW)',
     (0, 1200), np.arange(0, 1201, 200), 'uteffektlinear.png'),
    (power_dBm, 'RF uteffekt – dB-skala', 'Effekt (dBm)',
     (-30, 40), np.arange(-30, 41, 10), 'uteffektdecibel.png'),
]

for values, title, ylabel, limits, ticks, filename in plots:
    fig, ax = plt.subplots(figsize=(12, 6.75))
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.17, top=0.87)
    ax.plot(frequency_GHz, values, color='#0072BD', linewidth=0.85)
    ax.set(title=title, xlabel='Frekvens (GHz)', ylabel=ylabel,
           xlim=(0, 1), ylim=limits)
    ax.set_xticks(np.linspace(0, 1, 11))
    ax.set_yticks(ticks)
    ax.tick_params(length=6, pad=8)
    ax.grid(True, color='0.88', linewidth=0.7)
    ax.set_axisbelow(True)
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor='white')

plt.show()
