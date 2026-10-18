#pragma once
#include <Arduino.h>
#include <math.h>
#include "config.h"
#include "shows.h"

// 3 LEDs on LEDC PWM. Brightness is gamma-corrected so low levels look smooth.
class Lights {
 public:
  void begin() {
    for (int i = 0; i < LEDS; i++) {
      ledcSetup(i, LED_PWM_FREQ, LED_PWM_BITS);
      ledcAttachPin(PINS[i], i);
      ledcWrite(i, 0);
    }
  }

  void allOff() { for (int i = 0; i < LEDS; i++) write(i, 0); }

  // Update every LED for `elapsed` ms into `show`.
  void render(const Show& show, uint32_t elapsed) {
    int phase = min<uint32_t>(elapsed / PHASE_MS, PHASES - 1);
    uint32_t t = elapsed - phase * PHASE_MS;  // ms into this phase
    for (int i = 0; i < LEDS; i++) write(i, evaluate(show.lights[i][phase], t));
  }

  // Blink every LED once (boot self-test).
  void selfTest() {
    for (int i = 0; i < LEDS; i++) { write(i, 1.0f); delay(250); write(i, 0); }
  }

 private:
  const int PINS[LEDS] = {PIN_LED_TREX, PIN_LED_TRIKE, PIN_LED_SNAKE};

  void write(int ch, float v) {
    v = constrain(v, 0.0f, 1.0f);
    ledcWrite(ch, (uint32_t)(v * v * ((1 << LED_PWM_BITS) - 1)));  // gamma 2
  }

  // returns 0..1
  float evaluate(const Step& s, uint32_t t) {
    float peak = s.level / 255.0f;
    switch (s.pattern) {
      case P_OFF:    return 0;
      case P_ON:     return peak;
      case P_STROBE: return (t % s.period_ms) < (uint32_t)s.period_ms * s.duty / 100 ? peak : 0;
      case P_BREATHE: {
        float x = (t % s.period_ms) / (float)s.period_ms;
        return peak * (0.5f - 0.5f * cosf(2 * PI * x));  // starts dark, peaks mid-cycle
      }
      case P_HEARTBEAT: {  // lub (0-12%), dub (22-34%), rest
        float x = (t % s.period_ms) / (float)s.period_ms;
        float v = 0;
        if (x < 0.12f)                v = sinf(PI * x / 0.12f);
        else if (x > 0.22f && x < 0.34f) v = 0.7f * sinf(PI * (x - 0.22f) / 0.12f);
        return peak * v;
      }
      case P_FLICKER: {
        if (millis() - flickerAt_ > 35) {
          flickerAt_ = millis();
          flickerVal_ = 0.35f + 0.65f * (random(0, 1000) / 1000.0f);
        }
        return peak * flickerVal_;
      }
      case P_RAMP_UP:   return peak * (t / (float)PHASE_MS);
      case P_RAMP_DOWN: return peak * (1.0f - t / (float)PHASE_MS);
    }
    return 0;
  }

  uint32_t flickerAt_ = 0;
  float flickerVal_ = 1;
};
