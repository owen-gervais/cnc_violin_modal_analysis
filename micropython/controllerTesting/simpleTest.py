from machine import I2C, Pin
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu9250 import MPU9250
from utime import sleep

# Addresses 
MPU = 0x68
id = 0
sda = Pin(16)
scl = Pin(17)
impactThreshold = 18

# create the I2C
i2c = I2C(id=id, scl=scl, sda=sda)

# declare the MPU9250 class
m = MPU9250(i2c)

# We want a zero force
desired = 0
Kp = 50

while True:
    # filter the noise out of the y_acceleration
    y_acceleration = 0 if m.acceleration[2] < impactThreshold else m.acceleration[2] 
    
    # feedback loop error
    error = Kp*(desired - y_acceleration)
    
    if error: 
        print("error found!")
        print(error)
        
    motor.speed(error)
    sleep(0.002) # sleep and slow the loop down

