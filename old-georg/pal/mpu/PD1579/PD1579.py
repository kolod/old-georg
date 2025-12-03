from machine import Pin
import time

POWER  = Pin(0, Pin.OUT)

CLK    = Pin(1, Pin.OUT)
ACKN   = Pin(3, Pin.OUT)
A13    = Pin(4, Pin.OUT)
A14    = Pin(5, Pin.OUT)
A15    = Pin(6, Pin.OUT)
MODE0  = Pin(7, Pin.OUT)
S0     = Pin(8, Pin.OUT)
S1     = Pin(9, Pin.OUT)
IOM    = Pin(10, Pin.OUT)
MWAIT0 = Pin(11, Pin.OUT)
MWAIT1 = Pin(16, Pin.OUT)
MODE1  = Pin(26, Pin.OUT)

STATE0 = Pin(14, Pin.IN, None)
STATE1 = Pin(15, Pin.IN, None)
BSRE   = Pin(17, Pin.IN, None)
RAM1   = Pin(18, Pin.IN, None)
READY  = Pin(19, Pin.IN, None)
ROM1   = Pin(20, Pin.IN, None)
ROM0   = Pin(21, Pin.IN, None)
RAM0   = Pin(22, Pin.IN, None)

pause = 0.005

class PD1579:
    
    def __init__(self):
        self.state = 0
        self.set_state(0)
        CLK.off()
        ACKN.on()
        A13.off()
        A14.off()
        A15.off()
        MODE0.on()
        MODE1.on()
        S0.on()
        S1.on()
        MWAIT0.on()
        MWAIT1.on()
        POWER.off()
        
    def on(self):
        POWER.off()
        time.sleep(0.05)
        POWER.on()
        self.set_state(0)
        
    def off(self):
        POWER.off()
        time.sleep(0.05)
        
    def pause(self):
        time.sleep(0.005)
        
    def long_pause(self):
        for i in range(0,10):
            CLK.off()
            self.pause()
            CLK.on()
            self.pause()
            
    def set_mode(self, value):
        MODE0.value(value & 1)
        MODE1.value(value & 2)
        
    def set_state(self, value):
        if self.state == value:
            return
        
        if self.state == 0:
            if value == 1:
                CLK.off()
                IOM.on()
                self.set_mode(3)
                self.pause()
                CLK.on()
                self.pause()
                IOM.off()
            
            elif value == 2:
                CLK.off()
                IOM.on()
                self.set_mode(1)
                self.pause()
                CLK.on()
                self.pause()
                IOM.off()
            
            elif value == 3:
                CLK.off()
                IOM.on()
                self.set_mode(2)
                self.pause()
                CLK.on()
                self.pause()
                IOM.off()
                
        else:
            if value == 0:
                CLK.off()
                IOM.on()
                self.set_mode(3)
                self.pause()
                CLK.on()
                self.pause()
                IOM.off()
                
        self.state = value
    
    def set_fetch(self):
        S0.on();
        S1.on();
        
    def set_write(self):
        S0.on()
        S1.off()
        
    def set_read(self):
        S0.off()
        S1.on()
        
    def set_halt(self):
        S0.off()
        S1.off()
        
    def set_io(self):
        IOM.on()
        
    def set_mem(self):
        IOM.off()
        
    def set_addr(self, addr = 0x0000):
        A15.value(addr & 0x8000)
        A14.value(addr & 0x4000)
        A13.value(addr & 0x2000)
        
    def test_trigger(self):
        self.on()
        
        self.long_pause()
        self.set_state(1)
        self.long_pause()
        
        self.set_state(0)
        self.long_pause()
        
        self.set_state(2)
        self.long_pause()
        
        self.set_state(0)
        self.long_pause()
        
        self.set_state(3)
        self.long_pause()
        
        self.set_state(0)
        self.long_pause()
        
        self.off()
        
    def test_fetch(self, *modes):
        """ fetch can be only with IOM == 0 """
        for mode in modes:
            self.set_mode(mode)
            self.set_fetch()
            self.set_mem()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
            self.set_io()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
                
    def test_read(self, *modes):
        for mode in modes:
            self.set_mode(mode)
            self.set_read()
            self.set_mem()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
            self.set_io()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
                
    def test_write(self, *modes):
        for mode in modes:
            self.set_mode(mode)
            self.set_write()
            self.set_mem()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
            self.set_io()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
                
    def test_halt(self, *modes):
        for mode in modes:
            self.set_mode(mode)
            self.set_halt()
            self.set_mem()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
            self.set_io()
            for i in range(0, 0x10000, 0x2000):
                self.set_addr(i)
                self.long_pause()
        
        
    def test_state_0(self):
        self.on()
        
        self.set_state(0)        
        self.test_fetch(3)
        self.test_read(3)
        self.test_write(3)
        self.test_halt(3)
        
        self.off()
        
    def test_state_1(self):
        self.on()
        
        self.set_state(1)
        
        self.test_fetch(0)
        self.test_read(0)
        self.test_write(0)
        self.test_halt(0)
        
        self.test_fetch(1)
        self.test_read(1)
        self.test_write(1)
        self.test_halt(1)
        
        self.test_fetch(2)
        self.test_read(2)
        self.test_write(2)
        self.test_halt(2)
        
        self.off()
        
    def test_state_2(self):
        self.on()
        
        self.set_state(2)
        
        self.test_fetch(0)
        self.test_read(0)
        self.test_write(0)
        self.test_halt(0)
        
        self.test_fetch(1)
        self.test_read(1)
        self.test_write(1)
        self.test_halt(1)
        
        self.test_fetch(2)
        self.test_read(2)
        self.test_write(2)
        self.test_halt(2)
        
        self.off()
        
    def test_state_3(self):
        self.on()
        
        self.set_state(3)
        
        self.test_fetch(0)
        self.test_read(0)
        self.test_write(0)
        self.test_halt(0)
        
        self.test_fetch(1)
        self.test_read(1)
        self.test_write(1)
        self.test_halt(1)
        
        self.test_fetch(2)
        self.test_read(2)
        self.test_write(2)
        self.test_halt(2)
        
        self.off()
        
        
        
pld = PD1579()
pld.test_state_0()
time.sleep(0.2)
pld.test_state_1()
time.sleep(0.2)
pld.test_state_2()
time.sleep(0.2)
pld.test_state_3()

