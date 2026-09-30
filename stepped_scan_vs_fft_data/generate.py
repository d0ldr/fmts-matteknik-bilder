"""Simulate a stepped scan and an FFT (time-domain) scan of one example signal.

Writes the .dat files used by ../stepped_scan_vs_fft.tex (pgfplots).
All levels are in dBuV (RMS).  Run:  python3 generate.py
"""
import numpy as np

rng = np.random.default_rng(1)

# --- Example signal -----------------------------------------------------
# (name, frequency [MHz], level [dBuV], burst?)
TONES = [
    ("A", 104.03, 80.0, False),  # strong clock harmonic
    ("W", 105.02, 30.0, False),  # weak signal close to A (window demo)
    ("B", 111.53, 60.0, True),   # intermittent burst
    ("V", 121.01, 15.0, False),  # very weak signal (dynamic-range demo)
]
PHASE = {"A": 0.3, "W": 1.7, "B": 4.1, "V": 2.6}
BURST_ON, BURST_PERIOD, BURST_T0 = 5e-3, 0.5, 0.12   # 5 ms every 500 ms
RBW = 120e3
NOISE_DBUV = 0.0                     # noise floor in 120 kHz
N0 = 10 ** (NOISE_DBUV / 10) / RBW   # uV^2/Hz

F_LO, F_HI = 100.0, 125.0            # displayed span [MHz]


BURST_RAMP = 0.2e-3                  # smooth on/off ramps (no key clicks)


def burst_gate(t):
    tau = (t - BURST_T0) % BURST_PERIOD
    x = np.clip(np.minimum(tau, BURST_ON - tau) / BURST_RAMP, 0, 1)
    return (tau < BURST_ON) * (0.5 - 0.5 * np.cos(np.pi * x))


def signal(t, fc, fs, atten=None, noise=True):
    """Complex baseband (around fc [Hz]) of the example signal at times t."""
    z = np.zeros(t.shape, complex)
    for name, f, lev, burst in TONES:
        f = f * 1e6
        if abs(f - fc) > 0.45 * fs:
            continue
        a = np.sqrt(2) * 10 ** (lev / 20)
        if atten is not None:
            a *= 10 ** (-atten(f / 1e6) / 20)
        ph = PHASE[name]
        zz = a * np.exp(1j * (2 * np.pi * (f - fc) * t + ph))
        if burst:
            zz *= burst_gate(t)
        z += zz
    if noise:
        s = np.sqrt(2 * N0 * fs / 2)
        z += s * (rng.standard_normal(t.shape) + 1j * rng.standard_normal(t.shape))
    return z


def save(name, cols, header):
    np.savetxt(name, np.column_stack(cols), fmt="%.4f", header=header, comments="")


def dbuv_peak(zabs):
    return 20 * np.log10(np.maximum(zabs, 1e-3) / np.sqrt(2))


# --- Stepped scan ---------------------------------------------------------
def stepped(dwell, step=40e3, fs=0.5e6):
    freqs = np.arange(F_LO * 1e6, F_HI * 1e6 + 1, step)
    pad = 100e-6
    n = int(round((dwell + 2 * pad) * fs))
    fax = np.fft.fftfreq(n, 1 / fs)
    H = np.exp(-np.log(2) * (2 * fax / RBW) ** 2)       # Gaussian, 6 dB = RBW
    npad = int(pad * fs)
    out = []
    for k, fk in enumerate(freqs):
        t = k * dwell - pad + np.arange(n) / fs
        y = np.fft.ifft(np.fft.fft(signal(t, fk, fs)) * H)[npad:-npad]
        out.append(dbuv_peak(np.abs(y).max()))
    return freqs / 1e6, np.array(out), len(freqs) * dwell


# --- FFT scan -------------------------------------------------------------
FS, NFFT, HOP = 32e6, 512, 128          # 75 % overlap
FC = 112.5e6
WIN = np.hanning(NFFT)


def fft_levels(frames, win):
    X = np.fft.fftshift(np.fft.fft(frames * win, axis=-1), axes=-1)
    return np.abs(X) / win.sum()          # complex-envelope amplitude


def fft_freqs():
    return (FC + np.fft.fftshift(np.fft.fftfreq(NFFT, 1 / FS))) / 1e6


def adc(z, bits, fs_amp):
    if bits is None:
        return z
    d = 2 * fs_amp / 2 ** bits
    q = lambda x: np.clip(np.round(x / d) * d, -fs_amp, fs_amp - d)
    return q(z.real) + 1j * q(z.imag)


def fft_scan(duration, bits, atten=None):
    amps = [np.sqrt(2) * 10 ** ((lev - (atten(f) if atten else 0)) / 20)
            for _, f, lev, _ in TONES]
    fs_amp = 1.2 * sum(amps)               # full scale with some headroom
    frames_per_chunk = 4096
    L = HOP * (frames_per_chunk - 1) + NFFT
    ntot = int(duration * FS)
    pk = np.zeros(NFFT)
    av = np.zeros(NFFT)
    nfr = 0
    for start in range(0, ntot - NFFT, HOP * frames_per_chunk):
        m = min(L, ntot - start)
        t = (start + np.arange(m)) / FS
        z = adc(signal(t, FC, FS, atten), bits, fs_amp)
        fr = np.lib.stride_tricks.sliding_window_view(z, NFFT)[::HOP]
        a = fft_levels(fr, WIN)
        pk = np.maximum(pk, a.max(0))
        av += a.sum(0)
        nfr += len(fr)
    return fft_freqs(), dbuv_peak(pk), dbuv_peak(av / nfr), nfr


def in_span(f, lo=F_LO, hi=F_HI):
    return (f >= lo) & (f <= hi)


if __name__ == "__main__":
    # 1) one FFT frame, rectangular vs Hann window, ideal ADC, burst on
    t0 = BURST_T0 + 1e-3
    t = t0 + np.arange(NFFT) / FS
    z = signal(t, FC, FS)
    tus = (t - t0) * 1e6
    save("frame_time.dat", [tus, z.real / 1e3, (z * WIN).real / 1e3],
         "t_us I_mV Iw_mV")
    f = fft_freqs()
    s = in_span(f)
    for name, w in (("rect", np.ones(NFFT)), ("hann", WIN)):
        save(f"frame_{name}.dat", [f[s], dbuv_peak(fft_levels(z, w))[s]], "f L")

    # 2) stepped scans
    fr, lv, T = stepped(1e-3)
    print(f"stepped 1 ms: {len(fr)} points, {T:.3f} s")
    save("stepped_1ms.dat", [fr, lv], "f L")
    fr, lv, T = stepped(0.5)
    print(f"stepped 500 ms: {len(fr)} points, {T:.1f} s")
    save("stepped_500ms.dat", [fr, lv], "f L")

    # 3) FFT scans, same total time as the 1 ms stepped scan
    f, pk, av, n = fft_scan(0.625, bits=6)
    print(f"FFT scan: {n} frames")
    s = in_span(f)
    save("fft_peak.dat", [f[s], pk[s]], "f L")
    save("fft_avg.dat", [f[s], av[s]], "f L")

    # 4) FFT scan with a preselector that removes everything below 108 MHz
    presel = lambda fm: 60.0 if fm < 108 else 0.0
    f, pk, av, n = fft_scan(0.625, bits=6, atten=presel)
    s = in_span(f, 108, F_HI)
    save("fft_presel_peak.dat", [f[s], pk[s]], "f L")
