from machine import Pin, ADC
from motor import Motor
from count import Count
from utime import sleep


class ImpactHammerController():
    
    def __init__(self):
        
        # Constant declaration
        
        self.CONVERSION_FACTOR = 3.3 / 65535 # ADC conversion factor
        self.THRESHOLD = 0.02                # Threshold for impact hammer collision
        self.DESIRED_ANGLE = 90              # Angle set point for static positioning
        self.PULSE_TIME = 0.05
        self.DUTY_CYCLE = 100
        
        self.KP = 0.05                       # Proportional constant

        # Object instantiation

        self.triggerPin = Pin(14, Pin.IN, Pin.PULL_DOWN)        # Trigger interrupt pin for GCODE communication
        self.led = Pin(15, Pin.OUT)                             # Status LED object for monitoring trigger pin
        self.motor = Motor(Pin(21, Pin.OUT), Pin(20, Pin.OUT))  # DC motor object for hammer actuation
        self.encoder = Count(Pin(18, Pin.IN), Pin(19, Pin.IN))  # Encoder object to monitor hammer position
        self.adc = ADC(26)                                      # ADC_pin for feedback trigger monitor

        # System calibration and setup

        self.triggerPin.irq(trigger = Pin.IRQ_RISING, handler=controlLoop)   # Setup the interrupt callback function

        self.motor.mfloat()                  # Float the motor in order to allow for low impedance freefall
        self.encoder.calibrate()             # Zero the encoder (USER WILL MANUALLY SET THE HAMMER POST CALIBRATION)
    
    def controlLoop(self, irq):
        
        self.motor.pulse(self.DUTY_CYCLE, self.PULSE_TIME)      # Pulse the motor into freefall
        self.led.toggle()                                       # Trigger status led
        '''
        while True:
            reading = adc.read_u16() * self.CONVERSTION_FACTOR  # Read in input from the adc 
            if reading > self.THRESHOLD:                        # Logical true if impact
                prev_error = 0                                  
                while True:
                    error = self.DESIRED_ANGLE - self.encoder.angle   # Calculate setpoint error 
                    result = self.KP * error                          # Result speed
                    self.motor.speed(result)                          # Assign motor speed
                    if (LOWER_BOUND < result < UPPER_BOUND):          # Stop motor
                        self.motor.speed(0)
                        break
                    prev_error = error
                    sleep(0.001)
                break
            sleep(0.001)
          '''          
                    
if "__name__" == "__main__":
    
    hammer_controller = ImpactHammerController()

                    
                    
                    
                    
                    
                    

