/**
 * Copyright (C) 2025 Jabez Winston
 *
 * SPDX-License-Identifier: GPL-2.0-only
 *
 * @file    SimSerial.h
 * @brief   Simulated Console Serial module
 */

#ifndef PCSIM_SERTIAL_H
#define PCSIM_SERTIAL_H

#include "Stream.h"

#define SERIAL_TX_BUFFER_SIZE 64
#define SERIAL_RX_BUFFER_SIZE 64

typedef uint8_t tx_buffer_index_t;
typedef uint8_t rx_buffer_index_t;

class SimSerial : public Stream
{
  protected:
    // Has any byte been written to the UART since begin()
    bool _written;

    volatile rx_buffer_index_t _rx_buffer_head;
    volatile rx_buffer_index_t _rx_buffer_tail;
    volatile tx_buffer_index_t _tx_buffer_head;
    volatile tx_buffer_index_t _tx_buffer_tail;

    // Don't put any members after these buffers, since only the first
    // 32 bytes of this struct can be accessed quickly using the ldd
    // instruction.
    unsigned char _rx_buffer[SERIAL_RX_BUFFER_SIZE];
    unsigned char _tx_buffer[SERIAL_TX_BUFFER_SIZE];

public:
    void begin(long speed);
    void end(void);
    virtual int available(void);
    virtual int peek(void);
    virtual int read(void);
    // virtual int availableForWrite(void);
    virtual void flush(void);
    virtual size_t write(uint8_t);
    operator bool() { return true; }
};

extern SimSerial Serial;

#endif
