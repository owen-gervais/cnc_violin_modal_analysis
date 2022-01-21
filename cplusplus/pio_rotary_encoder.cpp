#include <stdio.h>
#include <iostream>

#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/irq.h"

#include "pio_rotary_encoder.pio.h"

// class to read the rotation of the rotary encoder
class Encoder
{
public:
    // Constructor
    Encoder(uint rotary_encoder_A)
    {
        uint8_t rotary_encoder_B = rotary_encoder_A + 1;
        PIO pio = pio0;   
        uint8_t sm = 0;   
        pio_gpio_init(pio, rotary_encoder_A);
        gpio_set_pulls(rotary_encoder_A, true, false);
        pio_gpio_init(pio, rotary_encoder_B);
        gpio_set_pulls(rotary_encoder_B, true, false);                      
        uint offset = pio_add_program(pio, &pio_rotary_encoder_program);
        pio_sm_config c = pio_rotary_encoder_program_get_default_config(offset);
        sm_config_set_in_pins(&c, rotary_encoder_A);                       
        sm_config_set_in_shift(&c, false, false, 0);                        
        irq_set_exclusive_handler(PIO0_IRQ_0, pio_irq_handler);
        irq_set_enabled(PIO0_IRQ_0, true);
        pio0_hw->inte0 = PIO_IRQ0_INTE_SM0_BITS | PIO_IRQ0_INTE_SM1_BITS;
        pio_sm_init(pio, sm, 16, &c);
        pio_sm_set_enabled(pio, sm, true);
    }

    // Set the current rotation to a specific value
    void set_rotation(int _rotation)
    {
        rotation = _rotation;
    }

    // get the current rotation
    int get_rotation(void)
    {
        return rotation;
    }

    int get_angle(void)
    {
        return rotation*6;
    }

private:
    static void pio_irq_handler()
    {
        // test if irq 0 was raised
        if (pio0_hw->irq & 1)
        {
            rotation = rotation - 1;
        }
        // test if irq 1 was raised
        if (pio0_hw->irq & 2)
        {
            rotation = rotation + 1;
        }
        // clear both interrupts
        pio0_hw->irq = 3;
    }

    // the pio instance
    PIO pio;
    // the state machine
    uint sm;
    // the current location of rotation
    static int rotation;
};