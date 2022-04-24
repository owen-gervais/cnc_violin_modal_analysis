#include "Motor.h"
#include "PWM.h"
#include "pico/stdlib.h"

// Default constructor
Motor::Motor()
    : PIN_A(20), PIN_B(21), FREQ(500)
{
}

// Non-default constructor
Motor::Motor(uint PIN_A, uint PIN_B)
{
    this->PIN_A = PIN_A;
    this->A = PWM(PIN_A, FREQ);
    this->PIN_B = PIN_B;
    this->B = PWM(PIN_B, FREQ);
}

// Speed 
void Motor::speed(int vel)
{
    if (vel < 0) {
        A.duty(-1*vel);
        B.duty(0);
    } else {
        A.duty(0);
        B.duty(vel);
    }
}

void Motor::pulse(int vel, int pulse_ms)
{
    speed(vel); // Turn on for set duty cycle
    sleep_ms(pulse_ms); // sleep for the pulse time
    speed(0);   // Shut off after sleep
}