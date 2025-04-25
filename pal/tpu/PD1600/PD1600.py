from machine import Pin
from time import sleep

POWER      = Pin(0, Pin.OUT)

READ       = Pin(1, Pin.OUT)
I0         = Pin(2, Pin.OUT)
I1         = Pin(3, Pin.OUT)
I2         = Pin(4, Pin.OUT)
I3         = Pin(5, Pin.OUT)
I4         = Pin(6, Pin.OUT)
I5         = Pin(7, Pin.OUT)
I6         = Pin(8, Pin.OUT)
I7         = Pin(9, Pin.OUT)
I8         = Pin(10, Pin.OUT)
I9         = Pin(11, Pin.OUT)
CE         = Pin(13, Pin.OUT)

Q9         = Pin(14, Pin.IN, None)
Q8         = Pin(15, Pin.IN, None)
Q7         = Pin(16, Pin.IN, None)
Q6         = Pin(17, Pin.IN, None)
Q5         = Pin(18, Pin.IN, None)
Q4         = Pin(19, Pin.IN, None)
Q3         = Pin(20, Pin.IN, None)
Q2         = Pin(21, Pin.IN, None)
Q1         = Pin(22, Pin.IN, None)
Q0         = Pin(26, Pin.IN, None)



def gray_code_generator(bits):
    if bits <= 0:
        raise ValueError("Number of bits must be a positive integer.")

    n = 1 << bits  # Total number of Gray codes (2^bits)
    for i in range(n):
        yield i ^ (i >> 1)  # Generate Gray code by applying the formula


class PD1600:
    
    def __init__(self):
        self.pause = 0.005
        POWER.off()        
        
    def on(self):
        CE.on()
        READ.on()
        sleep(0.001)
        POWER.on()
        sleep(0.01)
        
    def off(self):
        POWER.off()
        sleep(0.1)
        CE.on()
        READ.on()
        
    def set_data(self, value):
        I0.value(value & 0x0001)
        I1.value(value & 0x0002)
        I2.value(value & 0x0004)
        I3.value(value & 0x0008)
        I4.value(value & 0x0010)
        I5.value(value & 0x0020)
        I6.value(value & 0x0040)
        I7.value(value & 0x0080)
        I8.value(value & 0x0100)
        I9.value(value & 0x0200)
        
    def pull_up(self):
        Q9 = Pin(14, Pin.IN, Pin.PULL_UP)
        Q8 = Pin(15, Pin.IN, Pin.PULL_UP)
        Q7 = Pin(16, Pin.IN, Pin.PULL_UP)
        Q6 = Pin(17, Pin.IN, Pin.PULL_UP)
        Q5 = Pin(18, Pin.IN, Pin.PULL_UP)
        Q4 = Pin(19, Pin.IN, Pin.PULL_UP)
        Q3 = Pin(20, Pin.IN, Pin.PULL_UP)
        Q2 = Pin(21, Pin.IN, Pin.PULL_UP)
        Q1 = Pin(22, Pin.IN, Pin.PULL_UP)
        Q0 = Pin(26, Pin.IN, Pin.PULL_UP)
    
    def test_1(self):
        self.on()
        
        CE.off()        
        sleep(0.0001)
            
        READ.off()   
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        READ.on()
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        CE.on()
        sleep(self.pause)
            
        self.pull_up()
        sleep(self.pause)
        
        CE.off()        
        sleep(0.0001)
            
        READ.off()   
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        READ.on()
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        CE.on()
        sleep(self.pause)
        
        self.off()

    def test_2(self):
        self.on()
        
        CE.off()        
        sleep(0.0001)
            
        READ.off()   
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        READ.on()
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        CE.on()
        sleep(self.pause)
            
        self.pull_up()
        sleep(self.pause)
        
        CE.off()        
        sleep(0.0001)
            
        READ.off()   
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        READ.on()
        sleep(self.pause)
            
        self.set_data(0x5555)
        sleep(self.pause)
            
        self.set_data(0xAAAA)
        sleep(self.pause)
            
        CE.on()
        sleep(self.pause)
        
        self.off()


pd = PD1600()
pd.test_1()
pd.test_2()
