import random
from collections import namedtuple
from interfaces import ISensor, IActuator


class IPHDosingPump(IActuator):
    pass

class IPHSensor(ISensor):
    def read(self) -> float:
        return round(random.uniform(0.001, 14.000), 3)
        

WaterQualityResult = namedtuple('WaterQualityResult', ['ph_add_pump_status', 'ph_remove_pump_status'])
def controlWaterQuality(ph_value : float, min_ph : float, max_ph : float) -> WaterQualityResult:
    if ph_value < min_ph:
        return WaterQualityResult(True, False)
    elif ph_value > max_ph:
        return WaterQualityResult(False, True)
    else:
        return WaterQualityResult(False, False)
