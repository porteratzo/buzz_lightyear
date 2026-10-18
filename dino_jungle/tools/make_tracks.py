#!/usr/bin/env python3
"""Synthesize the Dino Jungle sound tracks.

Writes 16 kHz / 16-bit / mono WAVs to ../tracks and the same audio as C arrays
to ../src/tracks.h (compiled into flash, so no SD card or filesystem needed).

    python3 tools/make_tracks.py

Every sound is generated from scratch (noise, oscillators, filters), so there
are no licensing concerns. To use your own recordings instead, drop 16 kHz mono
WAVs over the files in tracks/ and run this script with --from-wav.
"""
import argparse
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

SR = 16000
HERE = Path(__file__).resolve().parent
TRACKS = HERE.parent / "tracks"
HEADER = HERE.parent / "src" / "tracks.h"
rng = np.random.default_rng(1234)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def bandpass(x, lo, hi, order=3):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lowpass(x, fc, order=3):
    return sosfilt(butter(order, fc, btype="low", fs=SR, output="sos"), x)


def highpass(x, fc, order=3):
    return sosfilt(butter(order, fc, btype="high", fs=SR, output="sos"), x)


def noise(n):
    return rng.standard_normal(n)


def env(n, attack, release):
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    e[:a] = np.linspace(0, 1, a)
    e[n - r:] = np.linspace(1, 0, r)
    return e


def norm(x, peak=0.9):
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def phase(freq):
    return 2 * np.pi * np.cumsum(freq) / SR


def saw(freq, harmonics=14):
    ph = phase(freq)
    return sum(np.sin(k * ph) / k for k in range(1, harmonics + 1))


# --------------------------------------------------------------------- tracks
def jungle_ambience(sec=6.0):
    """Seamless loop: wind/leaf rustle, insect drone, crickets, bird calls, frog."""
    n = int(sec * SR)
    t = t_axis(sec)
    wind = bandpass(noise(n), 200, 1200) * (0.5 + 0.5 * np.sin(2 * np.pi * t / sec * 2 + 1))
    rustle = bandpass(noise(n), 2500, 6000) * 0.15 * (0.6 + 0.4 * np.sin(2 * np.pi * t / sec * 3))
    # crickets: 4.6 kHz tone gated in rapid pulses
    gate = (np.sin(2 * np.pi * 28 * t) > 0.2) * (0.5 + 0.5 * np.sin(2 * np.pi * t / sec * 1))
    crickets = 0.12 * np.sin(2 * np.pi * 4600 * t) * lowpass(gate.astype(float), 60)
    # frog: low pulsing croak
    frog = np.zeros(n)
    for start in (1.1, 1.35, 3.9, 4.15, 4.4):
        i = int(start * SR)
        m = int(0.12 * SR)
        tt = np.arange(m) / SR
        frog[i:i + m] += 0.35 * np.sin(2 * np.pi * (260 - 400 * tt) * tt) * np.hanning(m)
    # birds: short FM chirps
    birds = np.zeros(n)
    for start, base in ((0.6, 2400), (2.4, 3000), (2.55, 3200), (4.8, 2700), (5.0, 3100)):
        i = int(start * SR)
        m = int(0.14 * SR)
        tt = np.arange(m) / SR
        f = base + 900 * np.sin(2 * np.pi * 22 * tt) + 1500 * tt
        birds[i:i + m] += 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(m)
    x = norm(wind * 0.8 + rustle + crickets + frog + birds, 0.55)
    # make it loop: crossfade the tail into the head
    xf = int(0.4 * SR)
    fade = np.linspace(0, 1, xf)
    x[:xf] = x[:xf] * fade + x[-xf:] * (1 - fade)
    return x[:-xf]


def trex_roar(sec=2.6):
    n = int(sec * SR)
    t = t_axis(sec)
    # pitch: quick rise then long falling roar, with wobble
    f0 = 55 + 70 * np.exp(-((t - 0.35) ** 2) / 0.05) + 25 * (1 - t / sec)
    f0 = f0 * (1 + 0.06 * np.sin(2 * np.pi * 7 * t))
    tone = saw(f0, 20)
    growl = (0.6 + 0.4 * np.sin(2 * np.pi * 32 * t))  # rough amplitude modulation
    mix = tone * growl + 0.8 * lowpass(noise(n), 900) * growl
    mix = bandpass(mix, 50, 3500)
    mix = np.tanh(3.0 * mix)                          # distortion = aggression
    amp = env(n, 0.05, 0.9) * (0.7 + 0.3 * np.exp(-t / 1.2))
    return norm(mix * amp)


def trike_bellow(sec=2.0):
    n = int(sec * SR)
    t = t_axis(sec)
    # two honking bellows with a snort in between
    f0 = 140 + 60 * np.sin(np.pi * np.clip(t / 0.8, 0, 1)) * (t < 0.8)
    f0 += (t >= 1.0) * (110 + 70 * np.sin(np.pi * np.clip((t - 1.0) / 0.9, 0, 1)))
    f0 *= 1 + 0.03 * np.sin(2 * np.pi * 5.5 * t)
    voice = saw(f0, 16)
    nasal = bandpass(voice, 300, 1400, 2) * 1.5 + voice * 0.3
    amp = np.zeros(n)
    amp[: int(0.85 * SR)] = np.hanning(int(0.85 * SR))
    amp[int(1.0 * SR): int(1.95 * SR)] = np.hanning(int(0.95 * SR))
    snort = highpass(lowpass(noise(n), 2500), 300) * 0.35
    snort *= np.exp(-((t - 0.92) ** 2) / 0.002)
    return norm(np.tanh(1.5 * nasal) * amp + snort)


def snake_hiss(sec=2.6):
    n = int(sec * SR)
    t = t_axis(sec)
    hiss = bandpass(noise(n), 3000, 7500, 4)
    swell = np.sin(np.pi * np.clip(t / 1.6, 0, 1)) ** 1.5 * (t < 1.6) \
        + 0.7 * np.sin(np.pi * np.clip((t - 1.6) / 1.0, 0, 1)) * (t >= 1.6)
    # rattle tail: fast amplitude pulses on noise
    rattle_gate = (np.sin(2 * np.pi * 24 * t) > 0) * (t > 1.0) * (t < 2.5)
    rattle = bandpass(noise(n), 1800, 6500) * lowpass(rattle_gate.astype(float), 120) * 0.8
    x = hiss * swell * 0.9 + rattle * env(n, 0.05, 0.3)
    return norm(x, 0.85)


TRACK_FUNCS = {
    "ambience": jungle_ambience,
    "trex": trex_roar,
    "trike": trike_bellow,
    "snake": snake_hiss,
}


# ------------------------------------------------------------------------ io
def to_int16(x):
    return (np.clip(x, -1, 1) * 32767).astype(np.int16)


def write_wav(path, data):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, \
            f"{path}: need {SR} Hz, mono, 16-bit"
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def write_header(tracks):
    lines = [
        "// GENERATED by tools/make_tracks.py -- do not edit by hand.",
        f"// {SR} Hz, 16-bit signed, mono. Stored in flash (PROGMEM).",
        "#pragma once",
        "#include <Arduino.h>",
        "",
        f"constexpr uint32_t TRACK_SAMPLE_RATE = {SR};",
        "",
    ]
    for name, data in tracks.items():
        lines.append(f"constexpr uint32_t TRACK_{name.upper()}_LEN = {len(data)};")
        lines.append(f"const int16_t TRACK_{name.upper()}[] PROGMEM = {{")
        for i in range(0, len(data), 16):
            lines.append("  " + ",".join(str(int(v)) for v in data[i:i + 16]) + ",")
        lines.append("};")
        lines.append("")
    HEADER.write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-wav", action="store_true",
                    help="skip synthesis; rebuild tracks.h from the WAVs already in tracks/")
    args = ap.parse_args()
    TRACKS.mkdir(exist_ok=True)
    tracks = {}
    for name, fn in TRACK_FUNCS.items():
        path = TRACKS / f"{name}.wav"
        if args.from_wav:
            data = read_wav(path)
        else:
            data = to_int16(fn())
            write_wav(path, data)
        tracks[name] = data
        print(f"{name:9s} {len(data) / SR:5.2f} s  {len(data) * 2 / 1024:6.1f} KB")
    write_header(tracks)
    total = sum(len(d) for d in tracks.values()) * 2 / 1024
    print(f"total {total:.0f} KB flash -> {HEADER}")


if __name__ == "__main__":
    main()
