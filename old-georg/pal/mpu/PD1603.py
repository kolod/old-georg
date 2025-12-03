from machine import Pin
from time import sleep

POWER  = Pin(0, Pin.OUT)
PCLK   = Pin(1, Pin.OUT)

A31    = Pin(2, Pin.OUT)
A30    = Pin(3, Pin.OUT)
A29    = Pin(4, Pin.OUT)
A28    = Pin(5, Pin.OUT)

A23    = Pin(6, Pin.OUT)
A22    = Pin(7, Pin.OUT)
A21    = Pin(8, Pin.OUT)
A20    = Pin(9, Pin.OUT)

RESET  = Pin(10, Pin.OUT)
ALE    = Pin(11, Pin.OUT)
READ   = Pin(13, Pin.OUT)
SIZE   = Pin(18, Pin.OUT)

MEM0   = Pin(22, Pin.IN, None)
MEM1   = Pin(14, Pin.IN, None)
MEM2   = Pin(26, Pin.IN, None)
LED    = Pin(15, Pin.IN, None)
INPUT  = Pin(16, Pin.IN, None)
BUS_IO = Pin(20, Pin.IN, None)
BUS_M  = Pin(21, Pin.IN, None)
Q6     = Pin(17, Pin.IN, None)
Q7     = Pin(19, Pin.IN, None)

CE     = Pin(14, Pin.OUT)


class PD1603:
    
    def __init__(self):
        self.pause = 0.005
        ALE.on()
        WRITE.on()
        READ.on()
        SIZE.off()
        RESET.off()
        
        
    def on(self, size):
        self.set_addr(0)
        SIZE.value(size)
        ALE.on()
        WRITE.on()
        READ.on()
        POWER.on()
        CE.on()
        sleep(self.pause)
        
    def off(self):
        POWER.off()
        sleep(0.1)
                
    def set_addr(self, value):
        A31.value(value & 0x80)
        A30.value(value & 0x40)
        A29.value(value & 0x20)
        A28.value(value & 0x10)
        A23.value(value & 0x08)
        A22.value(value & 0x04)
        A21.value(value & 0x02)
        A20.value(value & 0x01)
        
    def reset(self):
        RESET.on()
        sleep(0.01)
        RESET.off()
        sleep(self.pause)
        
    def write(self, addr):
        # T1
        PCLK.on()
        READ.on()
        ALE.on()
        self.set_addr(addr)
        sleep(self.pause)
        
        PCLK.off()
        sleep(self.pause)
        
        # T2
        ALE.off()
        sleep(self.pause)
        
        # T3, T4
        WRITE.off()
        sleep(self.pause)
        
        # T5, T6
        ALE.on()
        sleep(self.pause)
        WRITE.on()
        sleep(self.pause)
        
    def read(self, addr):
        # T1
        WRITE.on()
        READ.on()
        ALE.on()
        self.set_addr(addr)
        sleep(self.pause)
        
        # T2
        ALE.off()
        sleep(self.pause)
        
        # T3, T4
        READ.off()
        sleep(self.pause)
        
        # T5, T6
        ALE.on()
        sleep(self.pause)
        READ.on()
        sleep(self.pause)
        
    def test(self, size, *data):
        self.on(size)
        self.reset()
        
        for i in range(0, 256):
            self.write(i)
            self.read(i)
            
        self.off()
        
    def test_1MB(self):
        self.test(0)
        
    def test_4MB(self):
        self.test(1)

pd = PD1603()
pd.test_1MB()
pd.test_4MB()
