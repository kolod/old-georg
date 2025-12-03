from machine import Pin
from time import sleep

POWER  = Pin(0, Pin.OUT)
WRITE  = Pin(1, Pin.OUT)

A0     = Pin(2, Pin.OUT)
A1     = Pin(3, Pin.OUT)
A2     = Pin(4, Pin.OUT)
A3     = Pin(26, Pin.OUT)

D0     = Pin(5, Pin.OUT)
D1     = Pin(6, Pin.OUT)
D2     = Pin(7, Pin.OUT)
D3     = Pin(8, Pin.OUT)
D4     = Pin(9, Pin.OUT)
D5     = Pin(10, Pin.OUT)
D6     = Pin(11, Pin.OUT)
D7     = Pin(13, Pin.OUT)

Q0     = Pin(15, Pin.IN, Pin.PULL_UP)
Q1     = Pin(16, Pin.IN, Pin.PULL_UP)
Q2     = Pin(17, Pin.IN, Pin.PULL_UP)
Q3     = Pin(18, Pin.IN, Pin.PULL_UP)
Q4     = Pin(19, Pin.IN, Pin.PULL_UP)
Q5     = Pin(20, Pin.IN, Pin.PULL_UP)
Q6     = Pin(21, Pin.IN, Pin.PULL_UP)
Q7     = Pin(22, Pin.IN, Pin.PULL_UP)

CE     = Pin(14, Pin.OUT)


class PD1602:
    
    def __init__(self):
        self.pause = 0.005
        
        
    def on(self):
        self.set_addr(0)
        self.set_data(0)
        WRITE.on()
        POWER.on()
        CE.on()
        sleep(self.pause)
        
    def off(self):
        POWER.off()
        sleep(self.pause)
                
    def set_addr(self, value):
        A0.value(value & 0x01)
        A1.value(value & 0x02)
        A2.value(value & 0x04)
        A3.value(value & 0x08)
        
    def set_data(self, value):
        D0.value(value & 0x01)
        D1.value(value & 0x02)
        D2.value(value & 0x04)
        D3.value(value & 0x08)
        D4.value(value & 0x10)
        D5.value(value & 0x20)
        D6.value(value & 0x40)
        D7.value(value & 0x80)
        
    def write(self, addr, data):
        WRITE.on()
        CE.off()
        self.set_addr(addr)        
        self.set_data(data)
        sleep(self.pause)
        WRITE.off()
        sleep(self.pause)
        WRITE.on()
        sleep(self.pause)
        self.set_addr(0)
        self.set_data(0)
        CE.on()
        sleep(self.pause)
        
    def test(self, *data):
        self.on()
        
        for x in data:
            for i in range(0, 16):
                self.write(i, x)
            
        self.off()
        
    def test_2(self):
        self.on()
        
        self.write(0, 0)
        
        self.off()

pd = PD1602()
pd.test(0x00, 0x1, 0, 2)