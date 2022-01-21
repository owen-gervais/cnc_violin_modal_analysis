#include "pwm.h"
#include "pico/stdlib.h"
#include "hardware/pwm.h"

// Default constructor
PWM::PWM() 
    : PIN(20), SLICE(2), CHANNEL(0), FREQ(500), WRAP(0) 
{
}

// Non-default constructor
PWM::PWM(uint PIN, int FREQ) 
{
    this->PIN = PIN;                         
    this->FREQ = FREQ;
    this->SLICE = pwm_gpio_to_slice_num(PIN);
    this->CHANNEL = pwm_gpio_to_channel(PIN);
    generateConfiguration();
}

// Copy constructor
PWM::PWM(const PWM & other)
{
    copy(other);
}

// Assignment operator
PWM & PWM::operator=(const PWM& other){
    if (this != &other) {
        copy(other);
    }
    return *this;
}

// Setter function for duty cycle of PWM
void PWM::duty(int DUTY) {
    pwm_set_chan_level(SLICE, CHANNEL, WRAP * DUTY / 100);
}

// Getter function for pin of PWM
uint PWM::pin() const
{
    return PIN;
}

// Getter function for frequency of PWM
int PWM::freq() const
{
    return FREQ;
}

// Copy helper function
void PWM::copy(const PWM & other)
{
    this->PIN = other.pin();
    this->FREQ = other.freq();
    this->SLICE = pwm_gpio_to_slice_num(PIN);
    this->CHANNEL = pwm_gpio_to_channel(PIN);
    generateConfiguration();
}


void PWM::generateConfiguration()
{
    gpio_set_function(PIN, GPIO_FUNC_PWM);
    uint32_t divider16 = CLOCK / FREQ / 4096 + (CLOCK % (FREQ * 4096) != 0); 
    if (divider16 / 16 == 0)
    divider16 = 16;
    this->WRAP = CLOCK * 16 / divider16 / FREQ - 1;
    pwm_set_clkdiv_int_frac(SLICE, divider16/16, divider16 & 0xF);
    pwm_set_wrap(SLICE, WRAP);
    duty(0);
    pwm_set_enabled(SLICE, true);
}

