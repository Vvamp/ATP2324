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


def main_loop(f, ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump):    
    # Loop body
    return lambda: f(ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump) 

main = bet(lambda f: lambda ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump: main_loop(f, ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump))(ph_sensor, water_thermometer, room_thermometer, heater, cooler, increase_ph_pump, decrease_ph_pump)