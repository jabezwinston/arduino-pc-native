/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    SimSerial.cpp
 * @brief   Simulated Console Serial module
 */

#include "SimSerial.h"
#include <stdio.h>

SimSerial Serial;

void SimSerial::begin(long speed) {
    printf("[Serial.begin] Baud: %ld\n", speed);
}

void SimSerial::end()
{
  printf("[Serial.end]\n");
  // wait for transmission of outgoing data
  fflush(stdout);

  // clear any received data
  _rx_buffer_head = _rx_buffer_tail;
}

size_t SimSerial::write(uint8_t c) {
    putc(c, stdout);
    fflush(stdout);
    return 1;
}

int SimSerial::available()
{
  return ((unsigned int)(SERIAL_RX_BUFFER_SIZE + _rx_buffer_head - _rx_buffer_tail)) % SERIAL_RX_BUFFER_SIZE;
}

int SimSerial::read()
{
    getc(stdin);
    return 1;
}

int SimSerial::peek()
{
  if (_rx_buffer_head == _rx_buffer_tail) {
    return -1;
  } else {
    return _rx_buffer[_rx_buffer_tail];
  }
}

void SimSerial::flush()
{
    fflush(stdout);
}
