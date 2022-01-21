// Motor.h

#ifndef MOTOR_H
#define MOTOR_H

#include "pico/stdlib.h"
#include "PWM.h"

class Motor
{
    public: 
        // Default Constructor
        Motor(); 
        // Nondefault Constructor
        Motor(uint PIN_A, uint PIN_B);
        
        void speed(int vel);

        void pulse(int vel, int pulse_ms); 

    private:
        uint PIN_A;
        uint PIN_B;
        uint FREQ = 500;
        PWM A;
        PWM B;
};
#endif