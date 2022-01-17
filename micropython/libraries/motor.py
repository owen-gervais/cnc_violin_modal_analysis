from machine import PWM
from utime import sleep

class Motor():
    def __init__(self, A,B):
        self.A = PWM(A) # Creating a PWM object for motor phase A
        self.A.freq(500) # Establishing PWM frequency
        self.A.duty_u16(0) # Setting 0% duty cycle
        self.B = PWM(B) # Creating a PWM object for motor phase B
        self.B.freq(500) # Esablishing PWM frequency
        self.B.duty_u16(0) # Setting 0% duty cycle
        
    def u16(self,percent): # Helper function converting the speed to u16
        return int(percent * 65536) 
        
    def mbreak(self):
        self.A.duty_u16(0) # Set both PWM low in order to break
        self.B.duty_u16(0)
        
    def mfloat(self):
        self.A.duty_u16(self.u16(1)) #
        self.B.duty_u16(self.u16(1)) #

    def speed(self, vel):
        speed = self.u16(min(abs(vel/100),1)) # Define the speed of the motor
        a,b = (self.A,self.B) if vel < 0 else (self.B,self.A) # Reverse the direction if the comm
        a.duty_u16(0)  # to float between pulses, make this a 1
        b.duty_u16(speed)
        
    def pulse(self,vel,time):
        self.speed(vel)
        sleep(time)
        self.speed(0)

