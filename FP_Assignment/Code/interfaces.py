import random

class IActuator:
    def turnOn(self):
        pass
    def turnOff(self):
        pass

class ISensor:
    def read() -> float:
        return round(random.uniform(15.0, 35.9), 1)
