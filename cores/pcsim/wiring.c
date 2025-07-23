/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    wiring.c
 * @brief   Delay & Timer functions
 */

#include <stdint.h>

void delay(unsigned long ms)
{
    printf("[delay] Sleeping %lu ms\n", ms);
#if defined(__linux__)
    uint32_t delay_microsec = (uint32_t)(ms * 1000);
    usleep(delay_microsec);
#endif
}

void delayMicroseconds(unsigned int us)
{
#if defined(__linux__)
    usleep(us);
#endif
}

unsigned long millis()
{
    return (uint32_t)(clock());
}

unsigned long micros()
{
    return (uint64_t)(((uint64_t)clock()) * 1000);
}