//#include <cstdio>
#include <iostream>
#include "pico/stdlib.h"
// For PWM output: 
// For ADC input:
#include "hardware/adc.h"
#include "hardware/dma.h"
#include "hardware/pwm.h"
#include "pwm.h"
#include "motor.h"
#include "encoder.h"


int main() {
    stdio_init_all(); // Init all pins on the pico
    
    Motor motor = Motor(20, 21); // Initialize a motor object
    Encoder encoder = Encoder(18); // Initialize a PIO encoder object
    adc_init();
    // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(26);
    // Select ADC input 0 (GPIO26)
    adc_select_input(0);
    const float conversion_factor = 3.3f / (1 << 12);
    sleep_ms(15000);               // sleep for 15 to 
    encoder.set_rotation(0);        // zero the encoder by setting rotations to 0

    std::cout << "Ready to start test in 2 secs...." << std::endl;

    sleep_ms(2000);
    double KP = 2.4;
    motor.pulse(100, 8);
    while (true) {
        uint16_t result = adc_read();
        if ((result * conversion_factor) > 0.5) {
            int error = 0 - encoder.get_angle();
            double result = KP * error;
            motor.speed(result);
        }
    }
    return 0;
}