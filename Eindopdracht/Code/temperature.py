import random
from collections import namedtuple
        

TemperatureResult = namedtuple('TemperatureResult', ['heater_status', 'cooler_status'])
def controlWaterTemperature(water_temperature : float, room_temperature : float, target_temperature: int, target_temperature_deadzone : int = 3) -> TemperatureResult:
    max_temperature = target_temperature + target_temperature_deadzone
    min_temperature = target_temperature - target_temperature_deadzone

    # Turn on cooler or heater if outside safe ranges
    if water_temperature > max_temperature:
        return TemperatureResult(False, True)
    elif water_temperature < min_temperature:
        return TemperatureResult(True, False)
    
    # Turn on the heater/cooler if we expect the temperature to drop too much/raise too much based on room temperature. Otherwise, no cooling or heating necessary
    else:  
        if water_temperature < target_temperature and room_temperature < min_temperature:
            return TemperatureResult(True, False)
        elif water_temperature > target_temperature and room_temperature > max_temperature:
            return TemperatureResult(False, True)
        else:
            return TemperatureResult(False, False)
