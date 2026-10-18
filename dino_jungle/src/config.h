#pragma once
#include <Arduino.h>

// ---- Pins (see README.md for the wiring table) ----
constexpr int PIN_I2S_BCLK = 26;  // MAX98357A BCLK
constexpr int PIN_I2S_LRC  = 25;  // MAX98357A LRC (word select)
constexpr int PIN_I2S_DOUT = 22;  // MAX98357A DIN

constexpr int PIN_LED_TREX  = 16;
constexpr int PIN_LED_TRIKE = 17;
constexpr int PIN_LED_SNAKE = 18;

constexpr int PIN_BUTTON = 4;     // other leg of the button to GND (internal pull-up)

// ---- Behaviour ----
constexpr uint32_t PHASE_MS      = 5000;   // one light phase
constexpr int      PHASES        = 4;      // 4 x 5 s = 20 s show
constexpr uint32_t SHOW_MS       = PHASE_MS * PHASES;
constexpr uint32_t DEBOUNCE_MS   = 40;
constexpr bool     RESTART_ON_PRESS = false;  // true: a press during a show restarts it

// Master volume 0.0 - 1.0 (the MAX98357A GAIN pin sets the analog gain on top of this).
constexpr float MASTER_VOLUME  = 0.7f;
constexpr float AMBIENCE_LEVEL = 0.45f;  // jungle bed vs. the animal sounds
constexpr float ANIMAL_LEVEL   = 1.0f;

// LED PWM
constexpr int LED_PWM_FREQ = 5000;
constexpr int LED_PWM_BITS = 10;          // 0..1023
