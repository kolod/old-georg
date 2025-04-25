from machine import Pin
import time

CLK    = Pin(0, Pin.OUT)
ACKN   = Pin(2, Pin.OUT)
A13    = Pin(3, Pin.OUT)
A14    = Pin(4, Pin.OUT)
A15    = Pin(5, Pin.OUT)
MODE0  = Pin(6, Pin.OUT)
S0     = Pin(7, Pin.OUT)
S1     = Pin(8, Pin.OUT)
MODE1  = Pin(22, Pin.OUT)
IOM    = Pin(9, Pin.OUT)
MWAIT0 = Pin(10, Pin.OUT)
MWAIT1 = Pin(15, Pin.OUT)
POWER  = Pin(28, Pin.OUT)

pause = 0.005

def fetch():
    S0.on();
    S1.on();
    
def write():
    S0.on()
    S1.off()
    
def read():
    S0.off()
    S1.on()
    
def halt():
    S0.off()
    S1.off()

def start():
    POWER.off()
    print("Test")
    ACKN.off()
    CLK.off()
    A13.off()
    A14.off()
    A15.off()
    IOM.off()
    MODE0.on()
    MODE1.on()
    MWAIT0.on()
    MWAIT1.on()
    time.sleep(0.01)
    
    POWER.on()
    
def stop():
    time.sleep(0.01)
    POWER.off()
    
def set_io():
    CLK.off()
    IOM.on()
    time.sleep(pause)
    CLK.on()
    time.sleep(pause)
    
def set_memory():
    CLK.off()
    IOM.off()
    time.sleep(pause)
    CLK.on()
    time.sleep(pause)

def set_mode(mode0, mode1):
    set_io()
    CLK.off()
    time.sleep(pause/2)
    MODE0.value(mode0)
    MODE1.value(mode1)
    time.sleep(pause/2)
    CLK.on()
    time.sleep(pause)
    set_memory()
    
def set_addr(addr):
    CLK.off()
    time.sleep(pause/2)
    A15.value(addr & 4)
    A14.value(addr & 2)
    A13.value(addr & 1)
    time.sleep(pause/2)
    CLK.on()
    time.sleep(pause)
    CLK.off()
    time.sleep(pause)
    CLK.on()
    time.sleep(pause)

def all_addr():
    set_memory()
    for addr in range(0, 16):
        set_addr(addr)
        
    set_io()
    for addr in range(0, 16):
        set_addr(addr)

def main():
    start()
    
    # default M0=0 M1=0
    set_mode(1, 1)
    all_addr()
    
    # M0=1 M1=1
    set_mode(0, 1)    
    all_addr()
    
    # M0=1 M1=1
    set_mode(0, 0) 
    all_addr()
    
    # M0=1 M1=1
    set_mode(1, 0) 
    all_addr()
    
    # M0=1 M1=1
    set_mode(0, 0) 
    all_addr()
    
    # M0=1 M1=1
    set_mode(0, 1)    
    all_addr()
    
    # M0=1 M1=1
    set_mode(0, 0) 
    all_addr()
    
    # default M0=0 M1=0
    set_mode(1, 1)
    all_addr()
    
    # M0=1 M1=0
    set_mode(0, 0) 
    all_addr()
    
    # third
    set_mode(1, 0)
    all_addr()
    
    set_mode(0, 0) 
    all_addr()
    
    set_mode(0, 1)    
    all_addr()
    
    set_mode(0, 0) 
    all_addr()
    
    # default M0=0 M1=0
    set_mode(1, 1)
    all_addr()
    
    
    # M0=1 M1=1
    set_mode(1, 0)    
    all_addr()
    
    
    set_mode(0, 0) 
    all_addr()
    
    set_mode(0, 1)    
    all_addr()
    
    set_mode(0, 0) 
    all_addr()
    
    # default M0=0 M1=0
    set_mode(1, 1)
    all_addr()
    
    stop()
    time.sleep(0.5)
  
print("Start")  

halt()
main()

write()   
main()

fetch()
main()

read()
main()

print('End.')
