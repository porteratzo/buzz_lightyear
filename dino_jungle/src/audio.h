#pragma once
#include <Arduino.h>
#include <driver/i2s.h>
#include "config.h"
#include "tracks.h"
#include "shows.h"

// Mixer + MAX98357A output. A task on core 0 mixes the looping jungle bed with
// up to 3 simultaneous animal clips and streams stereo I2S (mono duplicated to
// both channels so the amp's L+R/2 mix doesn't halve the volume).
class AudioEngine {
 public:
  bool begin() {
    i2s_config_t cfg = {};
    cfg.mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX);
    cfg.sample_rate = TRACK_SAMPLE_RATE;
    cfg.bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT;
    cfg.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
    cfg.communication_format = I2S_COMM_FORMAT_STAND_I2S;
    cfg.intr_alloc_flags = ESP_INTR_FLAG_LEVEL1;
    cfg.dma_buf_count = 6;
    cfg.dma_buf_len = 256;
    cfg.tx_desc_auto_clear = true;  // silence (not noise) on underrun
    if (i2s_driver_install(I2S_NUM_0, &cfg, 0, nullptr) != ESP_OK) return false;

    i2s_pin_config_t pins = {};
    pins.mck_io_num = I2S_PIN_NO_CHANGE;
    pins.bck_io_num = PIN_I2S_BCLK;
    pins.ws_io_num = PIN_I2S_LRC;
    pins.data_out_num = PIN_I2S_DOUT;
    pins.data_in_num = I2S_PIN_NO_CHANGE;
    if (i2s_set_pin(I2S_NUM_0, &pins) != ESP_OK) return false;

    xTaskCreatePinnedToCore(taskEntry, "audio", 4096, this, 3, nullptr, 0);
    return true;
  }

  // Start the jungle bed; fades in over ~0.5 s.
  void startAmbience() { ambPos_ = 0; ambGain_ = 0; ambTarget_ = AMBIENCE_LEVEL; ambOn_ = true; }
  // Fade the bed out (sounds finish naturally).
  void stopAmbience() { ambTarget_ = 0; }
  void playClip(Clip c) {
    for (auto& v : voices_) {
      if (!v.active) { v.clip = c; v.pos = 0; v.active = true; return; }
    }  // all voices busy: drop the sound
  }
  void stopAll() { for (auto& v : voices_) v.active = false; ambTarget_ = 0; }
  bool ambienceAudible() const { return ambOn_; }

 private:
  struct Voice { volatile bool active = false; Clip clip = CLIP_TREX; uint32_t pos = 0; };
  Voice voices_[3];
  volatile bool ambOn_ = false;
  volatile float ambTarget_ = 0;
  float ambGain_ = 0;
  uint32_t ambPos_ = 0;

  static void taskEntry(void* self) { static_cast<AudioEngine*>(self)->run(); }

  static const int16_t* clipData(Clip c, uint32_t& len) {
    switch (c) {
      case CLIP_TREX:  len = TRACK_TREX_LEN;  return TRACK_TREX;
      case CLIP_TRIKE: len = TRACK_TRIKE_LEN; return TRACK_TRIKE;
      default:         len = TRACK_SNAKE_LEN; return TRACK_SNAKE;
    }
  }

  void run() {
    constexpr int N = 128;  // frames per block
    int16_t out[N * 2];
    const float fadeStep = 1.0f / (0.5f * TRACK_SAMPLE_RATE);
    for (;;) {
      for (int i = 0; i < N; i++) {
        float s = 0;
        if (ambOn_) {
          const float target = ambTarget_;
          if (ambGain_ < target) ambGain_ = min(target, ambGain_ + fadeStep);
          else if (ambGain_ > target) ambGain_ = max(target, ambGain_ - fadeStep);
          if (ambGain_ <= 0 && target <= 0) ambOn_ = false;
          s += (int16_t)pgm_read_word(&TRACK_AMBIENCE[ambPos_]) * ambGain_;
          if (++ambPos_ >= TRACK_AMBIENCE_LEN) ambPos_ = 0;
        }
        for (auto& v : voices_) {
          if (!v.active) continue;
          uint32_t len;
          const int16_t* d = clipData(v.clip, len);
          s += (int16_t)pgm_read_word(&d[v.pos]) * ANIMAL_LEVEL;
          if (++v.pos >= len) v.active = false;
        }
        s *= MASTER_VOLUME;
        // soft clip so overlapping roars don't crackle
        s = 32767.0f * tanhf(s / 32767.0f);
        int16_t q = (int16_t)s;
        out[2 * i] = q;
        out[2 * i + 1] = q;
      }
      size_t written;
      i2s_write(I2S_NUM_0, out, sizeof(out), &written, portMAX_DELAY);
    }
  }
};
