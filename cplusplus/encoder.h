//encoder.h

#ifndef ENCODER_H
#define ENCODER_H

#include <stdio.h>
#include <iostream>

#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/irq.h"

#include "pio_rotary_encoder.pio.h"

class Encoder
{
    public: 
        // Constructor
        Encoder(uint rotary_encoder_A);
        void set_rotation(int _rotation);
        int get_rotation(void);
        int get_angle(void);

    private:
        static void pio_irq_handler();
        PIO pio;
        uint sm;
        inline static int rotation = 0;
};
#endif