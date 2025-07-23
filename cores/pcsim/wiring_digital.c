/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    wiring_digital.c
 * @brief   Digital functions
 */

#include "Arduino.h"

void pinMode(int pin, int mode) { 
    printf("[pinMode] Pin %d set to %s\n", pin, mode == OUTPUT ? "OUTPUT" : "INPUT"); 
}
void digitalWrite(int pin, int val) { 
    printf("[digitalWrite] Pin %d = %d\n", pin, val); 
}
int digitalRead(int pin) { 
    printf("[digitalRead] Pin %d\n", pin); 
    return LOW; 
}