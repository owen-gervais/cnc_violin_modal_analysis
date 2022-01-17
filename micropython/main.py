from machine import Pin, ADC
from motor import Motor
from count import Count
from utime import sleep
from math import fabs


class ImpactHammerController():
    
    def __init__(self):
        
        # Constant declaration
        
        self.CONVERSION_FACTOR = 3.3 / 65535 # ADC conversion factor
        self.THRESHOLD = 0.5                # (V) Threshold for impact hammer collision
        self.DESIRED_ANGLE = 6.0             # Angle set point for static positioning
        self.PULSE_TIME = 0.005
        self.DUTY_CYCLE = 100
        self.OFFSET = 0
        
        self.KP = 2.8                       # Proportional constant
        self.KD = 0.001

        # Object instantiation

        self.triggerPin = Pin(14, Pin.IN, Pin.PULL_DOWN)        # Trigger interrupt pin for GCODE communication
        self.led = Pin(15, Pin.OUT)                             # Status LED object for monitoring trigger pin
        self.motor = Motor(Pin(21, Pin.OUT), Pin(20, Pin.OUT))  # DC motor object for hammer actuation
        self.encoder = Count(Pin(18, Pin.IN), Pin(19, Pin.IN))  # Encoder object to monitor hammer position
        self.adc = ADC(26)                                      # ADC_pin for feedback trigger monitor

        # System calibration and setup

        #self.triggerPin.irq(trigger = Pin.IRQ_RISING, handler=controlLoop)   # Setup the interrupt callback function

        self.motor.mfloat()                  # Float the motor in order to allow for low impedance freefall
        self.encoder.calibrate()
        
    def controlLoop(self):
        
        self.motor.pulse(self.DUTY_CYCLE, self.PULSE_TIME)      # Pulse the motor into freefall
        while True:
            reading = self.adc.read_u16() * self.CONVERSION_FACTOR  # Read in input from the adc
            if fabs(reading) > self.THRESHOLD: # Logical true if impact
                prev_error = 0
                while True:
                    error = self.DESIRED_ANGLE - self.encoder.angle   # Calculate setpoint error
                    if error == 6.0:
                        self.motor.speed(0)
                        break
                    derivative = error - prev_error
                    result = self.KP * error + self.KD * (derivative)
                    self.motor.speed(result)
                    #print(self.encoder.angle)
                    sleep(0.001)
                    
            #sleep(0.0001)
        
hammerCtrl = ImpactHammerController()
sleep(5)
hammerCtrl.controlLoop()


