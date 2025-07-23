/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    wiring_analog.c
 * @brief   Analog functions
 */

#include "Arduino.h"

void analogReference(uint8_t mode)
{
	printf("[%s] - mode=%u\n", __func__, mode);
}

int analogRead(uint8_t pin)
{
	printf("[%s] - pin=%u\n", __func__, pin);
	return 0;
}


void analogWrite(uint8_t pin, int val)
{
	printf("[%s] - pin=%u, val=%d\n", __func__, pin, val);
	pinMode(pin, OUTPUT);
	if (val == 0)
	{
		digitalWrite(pin, LOW);
	}
	else if (val == 255)
	{
		digitalWrite(pin, HIGH);
	}
}
