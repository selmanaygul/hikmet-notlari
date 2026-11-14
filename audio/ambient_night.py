#!/usr/bin/env python3
"""Gece ortam sesi: yumuşak rüzgâr + uzak cırcır böcekleri. Çalgı/müzik yok.
Kullanım: python3 audio/ambient_night.py <saniye> <çıktı.wav>"""
import sys, wave, numpy as np
dur = float(sys.argv[1]); out = sys.argv[2]
sr = 44100; n = int(sr*dur); t = np.arange(n)/sr
rng = np.random.default_rng(14)

def lowpass(x, a):  # tek kutuplu alçak geçiren
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a*(x[i]-acc); y[i] = acc
    return y

def wind(seed):
    r = np.random.default_rng(seed)
    w = lowpass(r.standard_normal(n), 0.02)
    w = lowpass(w, 0.05)
    gust = 0.55 + 0.45*np.sin(2*np.pi*t/7.3 + r.uniform(0, 6))*np.sin(2*np.pi*t/3.1 + r.uniform(0, 6))
    return w/np.abs(w).max()*gust

def crickets(f, rate, phase, gain):
    chirp_env = (np.sin(2*np.pi*rate*t + phase) > 0.55).astype(float)       # cır-cır darbeleri
    pulse = 0.5 + 0.5*np.sin(2*np.pi*30*t)                                   # her darbe içindeki titreşim
    groups = (np.sin(2*np.pi*t/2.2 + phase) > -0.3).astype(float)            # aralıklı gruplar
    env = lowpass(chirp_env*groups, 0.01)*pulse
    return np.sin(2*np.pi*f*t)*env*gain

L = 0.55*wind(1) + crickets(4300, 3.1, 0.0, 0.10) + crickets(4720, 2.7, 1.7, 0.06)
R = 0.55*wind(2) + crickets(4300, 3.1, 0.4, 0.07) + crickets(4720, 2.7, 1.2, 0.09)
st = np.stack([L, R], 1)
fade = int(sr*2.0); ramp = np.linspace(0, 1, fade)[:, None]
st[:fade] *= ramp; st[-fade:] *= ramp[::-1]
st = st/np.abs(st).max()*0.6
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st*32767).astype('<i2').tobytes())
