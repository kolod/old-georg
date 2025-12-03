from machine import Pin
from time import sleep

POWER      = Pin(0, Pin.OUT)

BCLK       = Pin(1, Pin.OUT)
RESET      = Pin(2, Pin.OUT)
BUS_EN     = Pin(3, Pin.OUT)
ALE        = Pin(4, Pin.OUT)
BPRN       = Pin(5, Pin.OUT)
XACK       = Pin(6, Pin.OUT)
PD1604_15  = Pin(7, Pin.OUT)
PD1597_17  = Pin(8, Pin.OUT)
WRITE      = Pin(9, Pin.OUT)

X1         = Pin(10, Pin.OUT)
X2         = Pin(11, Pin.OUT)
X3         = Pin(13, Pin.OUT)

Y1         = Pin(14, Pin.IN, None)
Y2         = Pin(15, Pin.IN, None)
Y3         = Pin(16, Pin.IN, None)
PD1604_16  = Pin(17, Pin.IN, None)
BUSY1      = Pin(18, Pin.IN, None)
BUSY2      = Pin(19, Pin.IN, None)
CBRQ1      = Pin(20, Pin.IN, None)
CBRQ2      = Pin(21, Pin.IN, None)
BREQ       = Pin(22, Pin.IN, None)
Y4         = Pin(26, Pin.IN, None)

def gray_code_generator(bits):
    if bits <= 0:
        raise ValueError("Number of bits must be a positive integer.")

    n = 1 << bits  # Total number of Gray codes (2^bits)
    for i in range(n):
        yield i ^ (i >> 1)  # Generate Gray code by applying the formula


class PD1598:
    
    def __init__(self):
        self.pause = 0.005
        POWER.off()        
        
    def on(self):
        sleep(0.001)
        RESET.off()
        POWER.on()
        sleep(0.01)
        
    def off(self):
        POWER.off()
        sleep(0.1)
        
    def pulse(self):
        sleep(self.pause)
        BCLK.off()
        sleep(self.pause)
        BCLK.on()
        sleep(self.pause)
        
    def reset(self):
        RESET.on()
        self.pulse()        
        RESET.off()
        sleep(self.pause)
        
    def test(self):
        
        self.on()
        self.reset()        
        
        for x in gray_code_generator(10):
            BUS_EN.value(x & 0x0001)
            ALE.value(x & 0x0002)
            BPRN.value(x & 0x0004)
            XACK.value(x & 0x0008)
            PD1604_15.value(x & 0x0010)
            PD1597_17.value(x & 0x0020)
            WRITE.value(x & 0x0040)
            X1.value(x & 0x0080)
            X2.value(x & 0x0100)
            X3.value(x & 0x0200)
            self.pulse()
            
        self.off()
        
        
    def test_breq(self):
        self.on()
        
        for x in [X1, X2, X3, WRITE, RESET, ALE, PD1604_15, PD1597_17]:
           
            X1.off()
            X2.off()
            X3.off()
            WRITE.off()
            BCLK.on()
            RESET.off()
            ALE.on()
            BPRN.off()
            PD1604_15.on()
            PD1597_17.on()
            sleep(self.pause)
            self.pulse()
            
            x.toggle()
            sleep(self.pause)
            self.pulse()
        
        self.off()


pd = PD1598()
pd.test()
#pd.test_breq()
