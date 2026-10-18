// Dino Jungle - kid's-room animal eyes + jungle sounds.
// ESP32 + MAX98357A I2S amp + speaker + 3 LEDs (T-rex, Triceratops, Snake) + button.
#include <Arduino.h>
#include "config.h"
#include "shows.h"
#include "lights.h"
#include "audio.h"

Lights lights;
AudioEngine audio;

enum State { IDLE, PLAYING };
State state = IDLE;
uint32_t showStart = 0;
int currentShow = -1;
uint8_t nextSound = 0;

// Button debounce: returns true once per press
bool buttonPressed() {
  static bool last = HIGH, stable = HIGH;
  static uint32_t changed = 0;
  bool now = digitalRead(PIN_BUTTON);
  if (now != last) { last = now; changed = millis(); }
  if (millis() - changed > DEBOUNCE_MS && now != stable) {
    stable = now;
    return stable == LOW;
  }
  return false;
}

// Random show, never the same one twice in a row
int pickShow() {
  int s;
  do { s = random(N_SHOWS); } while (s == currentShow && N_SHOWS > 1);
  return s;
}

void startShow() {
  currentShow = pickShow();
  nextSound = 0;
  showStart = millis();
  state = PLAYING;
  audio.stopAll();
  audio.startAmbience();
  Serial.printf("Show: %s\n", SHOWS[currentShow].name);
}

void endShow() {
  state = IDLE;
  audio.stopAmbience();
  lights.allOff();
  Serial.println("Show over - press the button again");
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  randomSeed(esp_random());
  lights.begin();
  if (!audio.begin()) Serial.println("I2S init FAILED - check pins");
  lights.selfTest();
  Serial.println("Dino Jungle ready");
}

void loop() {
  if (buttonPressed() && (state == IDLE || RESTART_ON_PRESS)) startShow();

  if (state == PLAYING) {
    uint32_t elapsed = millis() - showStart;
    const Show& show = SHOWS[currentShow];
    while (nextSound < show.n_sounds && elapsed >= show.sounds[nextSound].at_ms) {
      audio.playClip(show.sounds[nextSound].clip);
      nextSound++;
    }
    if (elapsed >= SHOW_MS) endShow();
    else lights.render(show, elapsed);
  }
  delay(5);  // ~200 Hz light updates
}
