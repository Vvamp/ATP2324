import typing, time
import temperature, quality

# Pybind imports
from Actuators.Relay import IRelay, Relay
from Sensors.DS18B20 import ISensor, DS18B20
from Sensors.MCP9808 import MCP9808
from Sensors.EzoPhCircuit import EzoPhCircuit


# https://stackoverflow.com/a/18506625
# Python doesn't have recursive tail optimization. Using a Y-combinator allows for an infinite looping function without using loops
def bet(func):
    b = (lambda f: (lambda x: x(x))(lambda y: f(lambda *args: lambda: y(y)(*args))))(
        func
    )

    def wrapper(*args):
        out = b(*args)
        while callable(out):
            out = out()
        return out

    return wrapper


ph_sensor = EzoPhCircuit(10, 11)
water_thermometer = DS18B20(5)
room_thermometer = MCP9808(6, 8)

heater = Relay(1)
cooler = Relay(2)
increase_ph_pump = Relay(3)
decrease_ph_pump = Relay(4)


def read_value(sensor: ISensor) -> float:
    return sensor.read()


def main_loop(
    f,
    ph_sensor,
    water_thermometer,
    room_thermometer,
    heater,
    cooler,
    increase_ph_pump,
    decrease_ph_pump,
):
    # Get values
    water_temperature, room_temperature, ph_value = map(
        read_value, [water_thermometer, room_thermometer, ph_sensor]
    )

    toggle_actuator: typing.Callable[[IRelay, bool], None] = (
        lambda actuator, actuator_state: actuator.turnOn()
        if actuator_state
        else actuator.turnOff()
    )

    # Check what states the actuators need to be set to
    temperature_states = temperature.controlWaterTemperature(
        water_temperature, room_temperature, 25, 3
    )
    ph_states = quality.controlWaterQuality(ph_value, 6.5, 7.5)

    # Apply the actuator states using map
    actuators = [heater, cooler, increase_ph_pump, decrease_ph_pump]
    states = [
        temperature_states.heater_status,
        temperature_states.cooler_status,
        ph_states.ph_add_pump_status,
        ph_states.ph_remove_pump_status,
    ]
    list(map(toggle_actuator, actuators, states))

    return lambda: f(
        ph_sensor,
        water_thermometer,
        room_thermometer,
        heater,
        cooler,
        increase_ph_pump,
        decrease_ph_pump,
    )

if __name__ == "__main__":
    main = bet(
        lambda f: lambda ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump: main_loop(
            f,
            ph_sensor,
            water_thermometer,
            room_thermometer,
            heater,
            cooler,
            increase_ph_pump,
            decrease_ph_pump,
        )
    )(
        ph_sensor,
        water_thermometer,
        room_thermometer,
        heater,
        cooler,
        increase_ph_pump,
        decrease_ph_pump,
    )


