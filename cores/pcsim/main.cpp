/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    main.cpp
 * @brief   Entry file for Arduino PC port
 */

#include "Arduino.h"

int main() {
    setup();
    for (;;) {
        loop();
    }
    return 0;
}
