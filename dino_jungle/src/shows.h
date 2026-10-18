#pragma once
#include <Arduino.h>
#include "config.h"

// ---------------------------------------------------------------------------
// A "show" is 20 s = 4 phases of 5 s. Each LED gets its own light pattern per
// phase, and each show has its own list of sound events. Every button press
// plays the next show (shuffled, never the same twice in a row).
// ---------------------------------------------------------------------------

enum Pattern : uint8_t {
  P_OFF,        // dark
  P_ON,         // steady glow at `level`
  P_STROBE,     // hard on/off; period = full cycle, duty = % on
  P_BREATHE,    // smooth sine fade; period = one full breath
  P_HEARTBEAT,  // lub-dub then rest; period = one beat
  P_FLICKER,    // random candle/menace flicker around `level`
  P_RAMP_UP,    // fade 0 -> level across the phase
  P_RAMP_DOWN,  // fade level -> 0 across the phase
};

struct Step {
  Pattern  pattern;
  uint16_t period_ms;  // cycle length (unused by OFF/ON/RAMP/FLICKER)
  uint8_t  duty;       // % on-time for STROBE
  uint8_t  level;      // peak brightness 0-255
};

enum Clip : uint8_t { CLIP_TREX, CLIP_TRIKE, CLIP_SNAKE };

struct SoundEvent {
  uint16_t at_ms;      // when in the 20 s show the clip starts
  Clip     clip;
};

constexpr int LEDS = 3;  // 0 = T-rex, 1 = Triceratops, 2 = Snake

struct Show {
  const char* name;
  Step        lights[LEDS][PHASES];
  SoundEvent  sounds[8];
  uint8_t     n_sounds;
};

// Shorthand to keep the tables readable
#define OFF            {P_OFF, 0, 0, 0}
#define ON(l)          {P_ON, 0, 0, l}
#define STROBE(p, d)   {P_STROBE, p, d, 255}
#define BREATHE(p, l)  {P_BREATHE, p, 0, l}
#define BEAT(p)        {P_HEARTBEAT, p, 0, 255}
#define FLICKER(l)     {P_FLICKER, 0, 0, l}
#define UP             {P_RAMP_UP, 0, 0, 255}
#define DOWN           {P_RAMP_DOWN, 0, 0, 255}

static const Show SHOWS[] = {
  {
    "Ambush",  // quiet jungle, snake slithers in, T-rex bursts out
    {
      /* T-rex  */ {OFF,            BREATHE(4000, 80),  STROBE(120, 50),  STROBE(80, 50)},
      /* Trike  */ {BREATHE(5000, 120), BREATHE(3000, 160), STROBE(200, 40), BREATHE(2500, 255)},
      /* Snake  */ {FLICKER(160),   STROBE(400, 15),    BREATHE(1500, 255), DOWN},
    },
    {{1200, CLIP_SNAKE}, {7500, CLIP_TRIKE}, {11000, CLIP_TREX}, {16500, CLIP_TREX}},
    4
  },
  {
    "Stampede",  // heavy flashing, everyone wakes up
    {
      /* T-rex  */ {BREATHE(2500, 140), STROBE(250, 50), BEAT(900), STROBE(100, 50)},
      /* Trike  */ {STROBE(500, 50),    BEAT(1100),      STROBE(160, 35), BREATHE(1200, 255)},
      /* Snake  */ {FLICKER(200),       STROBE(90, 50),  FLICKER(255), STROBE(300, 20)},
    },
    {{500, CLIP_TRIKE}, {4800, CLIP_TREX}, {9500, CLIP_SNAKE}, {12500, CLIP_TRIKE}, {17000, CLIP_TREX}},
    5
  },
  {
    "Stalker",  // slow, creepy, eyes open one at a time
    {
      /* T-rex  */ {OFF,   OFF,   UP,           STROBE(60, 50)},
      /* Trike  */ {OFF,   UP,    BREATHE(3000, 255), DOWN},
      /* Snake  */ {UP,    BREATHE(1800, 220), FLICKER(255), STROBE(200, 10)},
    },
    {{800, CLIP_SNAKE}, {6000, CLIP_TRIKE}, {10500, CLIP_SNAKE}, {14800, CLIP_TREX}},
    4
  },
  {
    "Heartbeat",  // pulsing, synchronized tension, then a flash roar
    {
      /* T-rex  */ {BEAT(1300), BEAT(900),  BEAT(600),  STROBE(70, 50)},
      /* Trike  */ {BEAT(1500), BEAT(1100), BEAT(750),  STROBE(110, 50)},
      /* Snake  */ {BREATHE(1000, 120), BREATHE(700, 180), BREATHE(450, 255), STROBE(55, 50)},
    },
    {{2000, CLIP_SNAKE}, {8000, CLIP_TRIKE}, {15200, CLIP_TREX}, {17500, CLIP_TREX}},
    4
  },
};
constexpr int N_SHOWS = sizeof(SHOWS) / sizeof(SHOWS[0]);
