/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    Tone.cpp
 * @brief   Tone functions
 */

 #include "Arduino.h"

void tone(uint8_t _pin, unsigned int frequency, unsigned long duration) {
    printf("[%s] - pin=%u, frequency=%u Hz, duration=%lu ms\n", __func__, _pin, frequency, duration);
}

void noTone(uint8_t _pin) {
    printf("[%s] - pin=%u (tone stopped)\n", __func__, _pin);
}
