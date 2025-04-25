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
WRITE  = Pin(14, Pin.OUT)
MEM_RF = Pin(20, Pin.OUT)

MEM0   = Pin(22, Pin.IN, None)
MEM2   = Pin(26, Pin.IN, None)
LED    = Pin(15, Pin.IN, None)
INPUT  = Pin(16, Pin.IN, None)
BUS_M  = Pin(21, Pin.IN, None)
Q6     = Pin(17, Pin.IN, None)
Q7     = Pin(19, Pin.IN, None)
SIZE   = Pin(18, Pin.IN, None)


class PD1604:
    
    def __init__(self):
        self.pause = 0.005
        ALE.on()
        PCLK.on()
        READ.on()
        WRITE.on()
        RESET.off()
        MEM_RF.off()
        
        
    def on(self):
        self.set_addr(0)
        ALE.on()
        PCLK.on()
        READ.on()
        WRITE.on()
        MEM_RF.off()
        RESET.off()
        POWER.on()
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
        
    def pulse(self, n = 1):
        for i in range(0, n):
            PCLK.on()
            sleep(self.pause)
            PCLK.off()
            sleep(self.pause)        
        
    def read(self, addr):
        # T1
        PCLK.on()
        READ.on()
        WRITE.on()
        ALE.on()
        self.set_addr(addr)
        self.pulse()
        
        # T2
        ALE.off()
        self.pulse()
        
        # T3, T4
        READ.off()
        self.pulse(8)
        
        # T5, T6
        ALE.on()
        self.pulse()
        READ.on()
        self.pulse()    
        
    def write(self, addr):
        # T1
        PCLK.on()
        READ.on()
        WRITE.on()
        ALE.on()
        self.set_addr(addr)
        self.pulse()
        
        # T2
        ALE.off()
        self.pulse(8)
        
        # T3, T4
        WRITE.off()
        self.pulse()
        
        # T5, T6
        ALE.on()
        self.pulse()
        WRITE.on()
        self.pulse()
        
    def test(self):
        self.on()        
        
        for i in range(0, 256):
            self.read(i)
            self.write(i)
            
        RESET.on()
        
        for i in range(0, 256):
            self.read(i)
            self.write(i)
        
        MEM_RF.on()
        RESET.off()
        
        for i in range(0, 256):
            self.read(i)
            self.write(i)
            
        RESET.on()
        
        for i in range(0, 256):
            self.read(i)
            self.write(i)
            
        self.off()
        
    def test_trigger_1(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.on()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(8)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        
    def test_trigger_2(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.on()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(2)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        
    def test_trigger_3(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.on()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(2)
        
        self.set_addr(0x00)
        self.pulse(6)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        
    def test_trigger_4(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.on()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(2)
        
        RESET.on()
        self.pulse(6)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        
    def test_trigger_5(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.on()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(2)
        
        MEM_RF.off()
        self.pulse(6)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        
    def test_trigger_6(self):
        self.on()
        
        ALE.on()
        WRITE.on()
        READ.on()
        MEM_RF.off()
        
        self.set_addr(0x70)
        self.pulse(8)
        
        ALE.off() 
        self.pulse(8)
        
        ALE.on() 
        self.pulse(8)
        
        self.off()
        

pd = PD1604()
pd.test_trigger_1()
pd.test_trigger_2()
pd.test_trigger_3()
pd.test_trigger_4()
pd.test_trigger_5()
pd.test_trigger_6()
pd.test()


