import unittest
from unittest.mock import MagicMock
from plant import *
from temperature import *
import main

from decorator import * 

# Pybind imports
from Actuators.Relay import IRelay, Relay
from Sensors.DS18B20 import ISensor, DS18B20
from Sensors.MCP9808 import MCP9808
from Sensors.EzoPhCircuit import EzoPhCircuit


simulator = Simulator()
def read_value_simulated(sensor: ISensor) -> float:
    return sensor.readSimulated(simulator.plant)


class TestSystem(unittest.TestCase):
    # Unit Tests
    @log
    def test_temperature_needs_raising(self):
        self.assertEqual(controlWaterTemperature(10, 5, 30), (True, False))
    @log
    def test_temperature_needs_nochange(self):
        self.assertEqual(controlWaterTemperature(30, 30, 30), (False, False))
    @log
    def test_temperature_needs_lowering(self):
        self.assertEqual(controlWaterTemperature(31, 35, 30), (False, True))
    @log
    def test_temperature_needs_nochange_deadzone(self):
        self.assertEqual(controlWaterTemperature(31, 20, 30), (False, False))

    # Integration Test (Tests if given a specific value, the right functions get called)
    def setUp(self):
        # Set up the sensor mocks
        self.ph_sensor = MagicMock(spec=ISensor)
        self.water_thermometer = MagicMock(spec=ISensor)
        self.room_thermometer = MagicMock(spec=ISensor)

        # Set up the actuator mocks
        self.heater = MagicMock(spec=IRelay)
        self.cooler = MagicMock(spec=IRelay)
        self.increase_ph_pump = MagicMock(spec=IRelay)
        self.decrease_ph_pump = MagicMock(spec=IRelay)

    def test_main_loop(self):
        # Configure the sensor mock return values
        self.ph_sensor.read.return_value = 7.0
        self.water_thermometer.read.return_value = 20.0
        self.room_thermometer.read.return_value = 15.0

        # Run the main loop once with the sensor values
        main.main_loop(
            lambda *args: None, 
            self.ph_sensor, 
            self.water_thermometer, 
            self.room_thermometer, 
            self.heater, 
            self.cooler, 
            self.increase_ph_pump, 
            self.decrease_ph_pump
        )

        # Assert the actuators were called correctly based on the sensor inputs
        self.heater.turnOn.assert_called_once()
        self.cooler.turnOff.assert_called_once()  # Assuming the control logic turns the cooler off at this temperature
        self.increase_ph_pump.turnOff.assert_called_once()  
        self.decrease_ph_pump.turnOff.assert_called_once()

    # System Test (Tests the system for 1000 iterations and checks if the turtle still lives(in a simulated environment))
    @log
    def test_system_test(self):
        ph_sensor = EzoPhCircuit(10, 11)
        water_thermometer = DS18B20(5)
        room_thermometer = MCP9808(6, 8)

        heater = Relay(1)
        cooler = Relay(2)
        increase_ph_pump = Relay(3)
        decrease_ph_pump = Relay(4)

        # Overwrite read value to use a simulated value
        main.read_value = read_value_simulated

        for i in range(0, 1000):
            main.main_loop(None, ph_sensor,
            water_thermometer,
            room_thermometer,
            heater,
            cooler,
            increase_ph_pump,
            decrease_ph_pump)

            simulator.runIteration(heater, cooler, increase_ph_pump, decrease_ph_pump)
        self.assertFalse(simulator.plant.aquarium.turtle.isDead)
