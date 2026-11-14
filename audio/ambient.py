#!/usr/bin/env python3
"""Ortam sesi kütüphanesi (müzik/çalgı yok, tamamen sentez; telif sorunu yok).

Kullanım: python3 audio/ambient.py <ses> <saniye> <çıktı.wav> [tohum]
Sesler: gece, gol, yagmur, dere, dalga, sabah, ates
Tohum (seed) her gönderide farklı verilirse aynı tür ses bile her seferinde farklı çıkar.
"""
import sys, wave
import numpy as np

SR = 44100


def band(x, lo, hi, soft=0.15):
    """FFT ile yumuşak kenarlı bant geçiren süzgeç."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    lo_e = 1 / (1 + np.exp(np.clip(-(f - lo) / (lo * soft + 1), -60, 60)))
    hi_e = 1 / (1 + np.exp(np.clip((f - hi) / (hi * soft + 1), -60, 60)))
    return np.fft.irfft(X * lo_e * hi_e, len(x))


def smooth(x, sec):
    """Hareketli ortalama (zarf yumuşatma)."""
    k = max(1, int(sec * SR))
    c = np.cumsum(np.concatenate([np.zeros(k), x]))
    return (c[k:] - c[:-k]) / k


def norm(x):
    m = np.abs(x).max()
    return x / m if m > 0 else x


class Gen:
    def __init__(self, dur, seed):
        self.n = int(dur * SR)
        self.t = np.arange(self.n) / SR
        self.r = np.random.default_rng(seed)
        self.dur = dur

    def noise(self):
        return self.r.standard_normal(self.n)

    def slow(self, period, depth=0.4):
        """Yavaş dalgalanan genlik (0..1)."""
        ph = self.r.uniform(0, 6.28)
        return 1 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * self.t / period + ph))

    def events(self, rate, fn, gain=1.0, jitter=(0.5, 1.0)):
        """Rastgele zamanlarda kısa olaylar (damla, cıvıltı, çıtırtı) yerleştirir."""
        out = np.zeros(self.n)
        k = self.r.poisson(rate * self.dur)
        for _ in range(k):
            ev = fn(self.r)
            st = self.r.integers(0, max(1, self.n - len(ev)))
            out[st:st + len(ev)] += ev * gain * self.r.uniform(*jitter)
        return out

    # --- tekil olaylar ---
    @staticmethod
    def drop(r):
        d = r.uniform(0.05, 0.12); t = np.arange(int(d * SR)) / SR
        f0 = r.uniform(700, 1400)
        f = f0 * (1 + 1.2 * t / d)                       # yukarı kayan "plip"
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 4))

    @staticmethod
    def chirp_bird(r):
        notes = []
        base = r.uniform(2500, 4800)
        for _ in range(r.integers(2, 6)):
            d = r.uniform(0.04, 0.11); t = np.arange(int(d * SR)) / SR
            sweep = r.uniform(-0.5, 0.6)
            f = base * (1 + sweep * t / d) + 300 * np.sin(2 * np.pi * r.uniform(20, 45) * t)
            env = np.sin(np.pi * t / d) ** 2
            notes.append(np.sin(2 * np.pi * np.cumsum(f) / SR) * env)
            notes.append(np.zeros(int(r.uniform(0.02, 0.08) * SR)))
            base *= r.uniform(0.85, 1.15)
        return np.concatenate(notes)

    @staticmethod
    def crackle(r):
        d = r.uniform(0.003, 0.02); t = np.arange(int(d * SR)) / SR
        return r.standard_normal(len(t)) * np.exp(-t / (d / 3))

    @staticmethod
    def frog(r):
        d = r.uniform(0.18, 0.35); t = np.arange(int(d * SR)) / SR
        f = r.uniform(160, 260)
        am = (np.sin(2 * np.pi * r.uniform(28, 40) * t) > 0).astype(float)
        return np.sin(2 * np.pi * f * t) * am * np.sin(np.pi * t / d)

    @staticmethod
    def bubble(r):
        d = r.uniform(0.01, 0.04); t = np.arange(int(d * SR)) / SR
        f = r.uniform(400, 1300) * (1 + 2.5 * t / d)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d / 3))

    def crickets(self, f, rate, gain):
        ph = self.r.uniform(0, 6)
        env = (np.sin(2 * np.pi * rate * self.t + ph) > 0.55).astype(float)
        env *= (np.sin(2 * np.pi * self.t / self.r.uniform(1.8, 3) + ph) > -0.3)
        env = smooth(env, 0.01) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * self.t))
        return np.sin(2 * np.pi * f * self.t) * env * gain

    def wind(self, lo=80, hi=600, period=7.0):
        return norm(band(self.noise(), lo, hi)) * self.slow(period, 0.55) * self.slow(period / 2.3, 0.3)


# --- sesler (sol, sağ) ---
def gece(g):
    ch = []
    for _ in range(2):
        ch.append(0.55 * g.wind() + g.crickets(4300, 3.1, 0.10) + g.crickets(4720, 2.7, 0.07))
    return ch


def gol(g):
    ch = []
    for _ in range(2):
        lap = norm(band(g.noise(), 150, 900)) * smooth(np.abs(np.sin(2 * np.pi * g.t / g.r.uniform(2.5, 3.5))), 0.3)
        x = 0.45 * lap + 0.25 * g.wind(60, 300, 9)
        x += g.events(0.9, g.drop, 0.35)
        x += g.events(0.5, g.frog, 0.12)
        x += g.crickets(4100, 2.9, 0.035)
        ch.append(x)
    return ch


def yagmur(g):
    ch = []
    for _ in range(2):
        hiss = norm(band(g.noise(), 900, 9000)) * g.slow(11, 0.25)
        body = norm(band(g.noise(), 200, 1200)) * 0.35
        x = 0.5 * hiss + body + g.events(25, g.crackle, 0.25)
        ch.append(x)
    rumble = norm(band(g.noise(), 25, 120)) * np.exp(-((g.t - g.dur * 0.55) / 1.6) ** 2)
    return [c + 0.6 * rumble for c in ch]


def dere(g):
    ch = []
    for _ in range(2):
        flow = norm(band(g.noise(), 250, 3000)) * (0.7 + 0.3 * smooth(g.r.random(g.n), 0.05) * 2)
        x = 0.4 * flow + g.events(35, g.bubble, 0.22) + 0.15 * g.wind(60, 250, 10)
        ch.append(x)
    return ch


def dalga(g):
    ch = []
    per = g.r.uniform(6.5, 8.5)
    for i in range(2):
        swell = smooth(np.clip(np.sin(2 * np.pi * g.t / per + i * 0.4), 0, None) ** 2, 0.4)
        surf = norm(band(g.noise(), 200, 5000)) * swell
        deep = norm(band(g.noise(), 40, 250)) * (0.4 + 0.6 * swell)
        ch.append(0.6 * surf + 0.5 * deep)
    return ch


def sabah(g):
    ch = []
    for _ in range(2):
        x = 0.25 * g.wind(100, 900, 8) + g.events(1.6, g.chirp_bird, 0.30)
        ch.append(x)
    return ch


def ates(g):
    ch = []
    for _ in range(2):
        roar = norm(band(g.noise(), 60, 400)) * g.slow(3, 0.4)
        x = 0.35 * roar + g.events(18, g.crackle, 0.6) + g.events(3, g.crackle, 1.2)
        ch.append(x)
    return ch


SOUNDS = {"gece": gece, "gol": gol, "yagmur": yagmur, "dere": dere, "dalga": dalga, "sabah": sabah, "ates": ates}


def make(name, dur, out, seed=0):
    g = Gen(dur, seed)
    L, R = SOUNDS[name](g)
    st = np.stack([L, R], 1)
    fade = int(SR * 1.5); ramp = np.linspace(0, 1, fade)[:, None]
    st[:fade] *= ramp; st[-fade:] *= ramp[::-1]
    st = st / np.abs(st).max() * 0.6
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 0)
