/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    WInterrupts.c
 * @brief   Interrupt functions
 */

#include <Arduino.h>
#include <stdint.h>

const char* modeToString(int mode) {
    switch (mode) {
        case LOW:     return "LOW";
        case CHANGE:  return "CHANGE";
        case RISING:  return "RISING";
        case FALLING: return "FALLING";
        default:      return "UNKNOWN";
    }
}

void attachInterrupt(uint8_t interruptNum, void (*userFunc)(void), int mode) {
    printf("[%s] - interruptNum=%u, mode=%s\n", __func__, interruptNum, modeToString(mode));
}

void detachInterrupt(uint8_t interruptNum) {
    printf("[%s] - interruptNum=%u\n", __func__, interruptNum);
}