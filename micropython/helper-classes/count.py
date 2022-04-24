from utime import sleep

class Count(object):
    def __init__(self,A,B):
        self.A = A
        self.B = B
        self.counter = 0
        self.rotation = 0
        self.angle = 0
        A.irq(self.cb,self.A.IRQ_FALLING|self.A.IRQ_RISING) #interrupt on line A
        B.irq(self.cb,self.B.IRQ_FALLING|self.B.IRQ_RISING) #interrupt on line B

    def cb(self,msg):
        other,inc = (self.B,1) if msg == self.A else (self.A,-1) #define other line and increment
        self.counter += -inc if msg.value()!=other.value() else  inc #XOR the two lines and increment
        self.rotation = self.counter/12/5
        self.angle = (self.rotation % 1) * 360
    
    def reset(self):
        self.counter = 0
        self.rotation = 0
        self.angle = 0
        
    def calibrate(self):
        print('----------------------------------------------------------------------')
        print('Calibrate the system to position 0. Encoder will reset in 5 seconds...')
        print('----------------------------------------------------------------------')
        for i in range(4):
            print("   " + str(4-i) + " seconds..")
            sleep(1)
        self.reset()
        print('----------------------------------------------------------------------')
        print("                            Encoder reset!                            ")
        print('----------------------------------------------------------------------')


