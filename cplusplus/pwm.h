// pwm.h

#ifndef PWM_H
#define PWM_H

#include "pico/stdlib.h"

class PWM 
{
    public: 
        // Default constructor
        PWM();
        // Nondefault constructor
        PWM(uint PIN, int FREQ);
        // Copy constructor
        PWM(const PWM & other);
        // Assign operator
        PWM & operator=(const PWM & other);

        void duty(int DUTY);
        uint pin() const;
        int freq() const;

    private:
        uint PIN;    // PWM driving pin
        uint SLICE;  // PWM Slice (determined from PIN)
        int CHANNEL; // PWM Slice Channel (determined from PIN)
        int FREQ;    // PWM Desired Frequency
        uint32_t WRAP;
        uint32_t CLOCK = 125000000; 

        void copy(const PWM & other);
        void generateConfiguration();
};
#endif