from machine import Pin, PWM, ADC, I2C
from motor import Motor
from count import Count
from mpu9250 import MPU9250
from utime import sleep
        
def pulseMotor(irq):
    global motor, led
    motor.pulse(100, 0.05)
    led.toggle()
        
gcodePin = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
motor = Motor(Pin(21, Pin.OUT),Pin(20, Pin.OUT))
encoder = Count(Pin(18, Pin.IN),Pin(19, Pin.IN))
i2c = I2C(id=0, scl=Pin(17), sda=Pin(16))
m = MPU9250(i2c)

motor.mfloat()
encoder.calibrate()

gcodePin.irq(trigger = Pin.IRQ_RISING, handler = pulseMotor)


# Control system design requirements
desired = 200
Kp = 1.9    # push back
Kd = 0.0
impactThreshold = 5


while True:
   # Filter the noise out of the y_acceleration
    y_acceleration = 0 if m.acceleration[2] < impactThreshold else m.acceleration[2]
    # Constant impulse off the surface
    if y_acceleration:
        
        #motor.pulse(100, 0.01)
        
        prev_error = 0
        derivative = 0
        
        while True:
            
            # Calculate feedback loop error
            
            error = desired - encoder.angle
            derivative = error - prev_error
            
            result = Kp*(error) + Kd*(derivative)
            
            
            motor.speed(-result)

            if (0 < result < 6):
                motor.speed(0)
                break
            
            prev_error = error
                
            sleep(0.001) # slow the loop
    sleep(0.001)
        

