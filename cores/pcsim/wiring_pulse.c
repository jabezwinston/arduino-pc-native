/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    wiring_pulse.c
 * @brief   Arduino Pulse functions
 */

#include <Arduino.h>
#include <stdint.h>
#include <stdio.h>

unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout)
{
	printf("[%s] - pin=%u, state=%u, timeout=%lu\n", __func__, pin, state, timeout);
	return 0;
}

unsigned long pulseInLong(uint8_t pin, uint8_t state, unsigned long timeout)
{
	printf("[%s] - pin=%u, state=%u, timeout=%lu\n", __func__, pin, state, timeout);
	return 0;
}
