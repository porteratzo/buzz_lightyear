# Dino Jungle 🦖🐍

Press a button and a kid's room comes alive: a 20-second jungle show with jungle
sounds, a T-rex roar, a Triceratops bellow and a snake hiss, while three LED
"eyes" (one per animal) breathe, strobe, flicker and heartbeat on their own timings.

## What you need

| Qty | Part | Notes |
|----|------|-------|
| 1 | ESP32 dev board (ESP32-WROOM "DevKit v1") | Any classic ESP32 works. S2/S3/C3 need a pin change and a different I2S API. |
| 1 | MAX98357A I2S amp breakout (Adafruit / generic) | 3 W mono class-D |
| 1 | Speaker, 4–8 Ω, 3 W | The bigger the cone, the better the T-rex sounds |
| 3 | LEDs (red/orange/green are fun) | Or 3 pairs of LEDs — see "Bigger eyes" |
| 3 | 150–220 Ω resistors | One per LED (use 100 Ω for dimmer 2 mA LEDs) |
| 1 | Momentary push button | Big arcade button is great for kids |
| 1 | USB 5 V supply, 1 A+ | A phone charger is fine |
| — | Breadboard/perfboard, wires | Solder it once it works |

## Wiring

```
                 ESP32                        MAX98357A
            ┌───────────┐                  ┌─────────────┐
            │      3V3  │                  │ VIN  ◄──────┼── 5V (ESP32 "VIN"/USB 5V pin)
            │       GND ├──────────────────┤ GND         │
            │   GPIO 26 ├──────────────────┤ BCLK        │
            │   GPIO 25 ├──────────────────┤ LRC         │
            │   GPIO 22 ├──────────────────┤ DIN         │    ┌─ speaker +
            │           │                  │ SD    (leave)│    │
            │           │                  │ GAIN  (leave)│  + ├─ speaker −
            └───────────┘                  │ out+ / out− ─┼────┘
                                           └─────────────┘
```

| ESP32 | Goes to | Purpose |
|-------|---------|---------|
| GPIO 26 | MAX98357A **BCLK** | I2S bit clock |
| GPIO 25 | MAX98357A **LRC** | I2S word select |
| GPIO 22 | MAX98357A **DIN** | I2S data |
| 5V (VIN) | MAX98357A **VIN** | Amp power (5 V = louder than 3.3 V) |
| GND | MAX98357A **GND** | |
| — | MAX98357A **+ / −** | Speaker (this is the amp output, not a signal) |
| GPIO 16 | LED 1 (T-rex) via resistor → GND | |
| GPIO 17 | LED 2 (Triceratops) via resistor → GND | |
| GPIO 18 | LED 3 (Snake) via resistor → GND | |
| GPIO 4 | Button → GND | Internal pull-up is on, no resistor needed |

LED wiring: `GPIO ── resistor ── LED anode (long leg) … LED cathode (short leg) ── GND`

Amp pin notes:
- **SD**: leave unconnected — that gives (L+R)/2 mono. The firmware sends the same audio on both channels so nothing is lost.
- **GAIN**: unconnected = 9 dB (default). To GND = 12 dB, to VIN = 6 dB, via 100 kΩ to GND = 15 dB. Volume is also software-adjustable: `MASTER_VOLUME` in `src/config.h`.
- Add a 470–1000 µF capacitor across the amp's VIN/GND if you hear popping at high volume.

### Bigger eyes
An ESP32 pin should drive ≤ ~12 mA. For two LEDs per animal wire them in **parallel, each with its own resistor** (≤ 20 mA total per pin is OK for brief use) or, better, drive each eye with a small transistor: GPIO → 1 kΩ → base of a 2N2222/2N7000-style NPN, LED + resistor from 5 V to the collector, emitter to GND. For LED strips use a logic-level MOSFET.

## Software

1. Install [PlatformIO](https://platformio.org/) (VS Code extension or `pip install platformio`).
2. `cd dino_jungle && pio run -t upload` then `pio device monitor`.
3. On boot each LED blinks once (self-test). Press the button: show starts.

Behaviour:
- Press while idle → plays a random show (never the same twice in a row).
- Press during a show → ignored (set `RESTART_ON_PRESS = true` in `src/config.h` to restart instead).
- Show = 4 phases × 5 s = 20 s. Each LED has its own pattern per phase.
- Jungle ambience fades in at the start and out at the end; animal clips land at timed moments per show.

### The four shows (edit freely in `src/shows.h`)
| Show | Feel |
|------|------|
| **Ambush** | Quiet jungle, snake slithers in, then the T-rex bursts out strobing |
| **Stampede** | Everything awake — flashing and heartbeat, overlapping roars |
| **Stalker** | Eyes open one by one (snake → trike → T-rex), slow and creepy |
| **Heartbeat** | Synchronized pulses speed up, ending with a strobe roar |

Light patterns: `OFF, ON, STROBE(period, duty%), BREATHE(period, level), BEAT(period), FLICKER(level), UP, DOWN`.
Adding a show = add one more entry to `SHOWS[]`; the sound list is `{start_ms, clip}`.

## Code layout

```
dino_jungle/
├── platformio.ini
├── src/
│   ├── config.h      pins, volume, timing
│   ├── shows.h       the light + sound timelines (edit this to change the show)
│   ├── lights.h      LED PWM patterns (gamma-corrected)
│   ├── audio.h       I2S mixer: looping ambience + 3 overlapping animal voices
│   ├── tracks.h      GENERATED audio arrays (stored in flash)
│   └── main.cpp      button debounce + show state machine
├── tools/make_tracks.py   synthesizes the audio, writes tracks/*.wav and src/tracks.h
└── tracks/           ambience, trex, trike, snake (16 kHz, 16-bit, mono WAV)
```

## Tracks

All four are synthesized by `tools/make_tracks.py` (numpy/scipy), so there are no licensing issues. Total 400 KB of flash.

| File | Length | Content |
|------|--------|---------|
| `ambience.wav` | 5.6 s, seamless loop | Wind, leaf rustle, crickets, bird chirps, frog croaks |
| `trex.wav` | 2.6 s | Distorted, growling, falling-pitch roar |
| `trike.wav` | 2.0 s | Two nasal bellows with a snort |
| `snake.wav` | 2.6 s | Hiss swelling into a rattle |

They are synthetic, so they sound more "arcade" than "nature documentary". To upgrade, replace any WAV in `tracks/` with a real recording (16 kHz, mono, 16-bit — `ffmpeg -i in.wav -ar 16000 -ac 1 -sample_fmt s16 tracks/trex.wav`), then run `python3 tools/make_tracks.py --from-wav` to rebuild `src/tracks.h`. Keep the total under ~1 MB for the default partition; for longer audio, switch to LittleFS or an SD card.

## Status / testing

- Light patterns and the show tables compile and run on a host test harness.
- The audio tracks were generated and sanity-checked (levels, no clipping/NaN).
- **The full ESP32 firmware has not been compiled or flashed yet** — the build environment couldn't download the ESP32 toolchain. Expect to fix small things on first build, and tune `MASTER_VOLUME` / `AMBIENCE_LEVEL` by ear.

## Troubleshooting
- **No sound**: check BCLK/LRC/DIN aren't swapped; check amp VIN has 5 V; the serial monitor prints `I2S init FAILED` if the driver didn't start.
- **Hissing/noise when idle**: normal for some amps; tie SD to GND via a GPIO if you want to mute it between shows.
- **ESP32 resets when the roar plays**: weak USB supply or cable; use a 1 A+ charger and add the bulk capacitor.
- **Won't compile on Arduino-ESP32 3.x**: `platformio.ini` pins espressif32@6 (core 2.x) because `audio.h` uses the legacy I2S driver.
