import typing, time
import temperature, quality
from interfaces import IActuator, ISensor

# https://stackoverflow.com/a/18506625 
# Python doesn't have recursive tail optimization. Using a Y-combinator allows for an infinite looping function without using loops
def bet(func):
    b = (lambda f: (lambda x: x(x))(lambda y:
          f(lambda *args: lambda: y(y)(*args))))(func)
    def wrapper(*args):
        out = b(*args)
        while callable(out):
            out = out()
        return out
    return wrapper


ph_sensor = quality.IPHSensor()
water_thermometer = temperature.IThermometer()
room_thermometer = temperature.IThermometer()
heater = temperature.IHeater()
cooler = temperature.ICooler()
increase_ph_pump = quality.IPHDosingPump()
decrease_ph_pump = quality.IPHDosingPump()

def read_value(sensor: ISensor) -> float:
    return sensor.read()

def main_loop(f, ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump):    
    # Get values
    water_temperature, room_temperature, ph_value = map(read_value, [water_thermometer, room_thermometer, ph_sensor])

    toggle_actuator : typing.Callable[[IActuator,bool], None] = lambda actuator, actuator_state : actuator.turnOn() if actuator_state else actuator.turnOff()
    
    # Check what states the actuators need to be set to 
    temperature_states = temperature.controlWaterTemperature(water_temperature, room_temperature, 30,  3)
    ph_states = quality.controlWaterQuality(ph_value, 6.5, 7.5)
        
    # Apply the actuator states using map
    actuators = [heater, cooler, increase_ph_pump, decrease_ph_pump]
    states = [temperature_states.heater_status, temperature_states.cooler_status, ph_states.ph_add_pump_status, ph_states.ph_remove_pump_status]
    list(map(toggle_actuator, actuators, states))

    return lambda: f(ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump) 

main = bet(lambda f: lambda ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump: main_loop(f, ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump))(ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump)