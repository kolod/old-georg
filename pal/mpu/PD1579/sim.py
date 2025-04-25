from machine import Pin
from time import sleep


class Simulator:

    def __init__(self):
        self.vectors = []
        self.pins = []
        self.power = Pin(0, Pin.OUT)
        self.error = ''
        self.pins_cache = {}
        self.pin_map = [None,1,2,3,4,5,6,7,8,9,10,11,None,13,14,15,16,17,18,19,20,21,22,26,None]

    def pause(self):
        sleep(0.0001)

    def on(self):
        self.power.on()
        self.pause()

    def off(self):
        self.power.off()
        self.pause()

    def set_vectors(self, vectors):
        self.vectors = vectors

    def set_pins(self, pins):
        self.pins = pins

    def simulate(self):
        self.on()
        for vector in self.vectors:
            if not self._simulate(vector.strip().lower()):
                print(f'Vector {vector} failed with {self.error}\n')
        self.off()

    def _clock(self, pin):
        if pin < 0:
            return
        
        self._set_pin(pin, 0)
        self.pause()
        self._set_pin(pin, 1)
        self.pause()

    def _set_pin(self, pin, value):
        if (pin < 0) or (pin >= len(self.pins)):
            return
        
        #print(f"set pin {pin} to {value}")
        if pin not in self.pins_cache:
            self.pins_cache[pin] = Pin(self.pin_map[self.pins[pin]], Pin.OUT)
        self.pins_cache[pin].value(value)

    def _get_pin(self, pin):
        if pin not in self.pins_cache:
            self.pins_cache[pin] = Pin(self.pin_map[self.pins[pin]], Pin.IN, None)
        return self.pins_cache[pin].value()

    def _test(self, pin, value):
        if value == 'L' and self._get_pin(pin) == 0:
            return True
        
        if value == 'H' and self._get_pin(pin) == 1:
            return True
        
        # TODO: check high z
        return False

    def _simulate(self, vector):
        print(vector)
        print(f'c count = {vector.count('c')}')

        # check if only one 'C' in vector
        if vector.count('c') > 1:
            self.error = 'Too many `C` in vector'

        # get clock pin if neaded
        clock = vector.find('c')

        # count all 'x'
        xpins = [i for i, char in enumerate(vector) if char == 'x']
        print(f'xpins = {str(xpins)}')

        for i, value in enumerate(vector):
            if value == '0':
                self._set_pin(i, 0)
            elif value == '1':
                self._set_pin(i, 1)
            
        for i in range(0, 1 << len(xpins)):
            for pin in xpins:
                self._set_pin(pin, i & pin)
                self._clock(clock)

                for j, value in enumerate(vector):
                    if value in 'HLZ':
                        if not self._test(j, value):
                            self.error = f'pin {self.pins[j]} must be {value}'
                            return False

        self.error = ''            
        return True


sim = Simulator()
sim.set_pins([1, 3, 4, 5, 6, 7, 23, 8, 9, 10, 11, 16, 14, 15, 19, 17, 21, 20, 22, 18])
sim.set_vectors([
    'CXXXX11XXXXXLL******',
    'CXXX011XX0XXLL*HLHHH',
    'CXXX111XX0XXLL*HHHHL'
])
sim.simulate()
