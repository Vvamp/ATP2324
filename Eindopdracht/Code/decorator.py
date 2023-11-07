from functools import wraps
from collections import deque
import random, time, statistics

# Logs which function was run and with what arguments
def log(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            print("Entering: [%s] with parameters %s" % (func.__name__, args))
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('Exception in %s : %s' % (func.__name__, e))
        finally:
            print("Exiting: [%s]" % func.__name__)
    return wrapped

# Has a specified chance of sending an out-of-bounds value.
# This simulates a failing sensor
def simulate_potential_fail(lower_limit, upper_limit, failing_chance : float = 0.5):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if random.random() < failing_chance:
                print(f"Simulating failing sensor. Lower limit: {lower_limit}. Upper limit: {upper_limit}")
                return random.choice([lower_limit-1, upper_limit+1, lower_limit-lower_limit*0.8, upper_limit+lower_limit*0.8]) # Return a random failing number
            return func(*args, **kwargs)
        return wrapped
    return decorator

# Measures the time since the last sensor reading. 
# This can be used for performance testing, but also to verify how often we poll the data
def time_sensor_readings(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        current_time = time.perf_counter()
        if wrapped.lastvalue != None:
            wrapped.timings.append(current_time - wrapped.lastvalue)
        wrapped.lastvalue = current_time
        return func(*args, **kwargs)
    wrapped.timings = []
    wrapped.lastvalue = None
    return wrapped

# Detects a sudden outlier based on a specified number of previous readings and a percentage(how much the reading can deviate from the mean)
# This can help detecting sensor malfunctions, as it's not common for a sensor to give a substantial higher/lower reading than the mean(given the sensor is polled enough).
def notify_sudden_increase(cached_readings : int = 4, change_percentage : float = 0.9):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            wrapped.cached_values.append(result)

            # Check if the last value is a sudden outlier
            if(wrapped.cached_values.maxlen == len(wrapped.cached_values)):
                cached_mean = statistics.mean(wrapped.cached_values)

                # Calculate the percentage increase based on the mean
                current_change = abs((result - cached_mean) / cached_mean)
                if(current_change > change_percentage):
                    higher_text = "higher" if result > cached_mean else "lower"
                    wrapped.outliers_with_means.append((result, cached_mean))
                    print(f"Sudden outlier! {result} is {current_change*100}% {higher_text} than the mean('{cached_mean}') of the last {cached_readings} readings")
            return result
        wrapped.cached_values = deque(maxlen=cached_readings)
        wrapped.outliers_with_means = []
        return wrapped 
    return decorator


# Example of how my water thermometer's read might function
@time_sensor_readings
@log
@simulate_potential_fail(-55, 125, 0.1)
def read_thermometer():
    return random.randint(-55, 125)


# Example of how my pH sensor's read might function
@time_sensor_readings
@log
@notify_sudden_increase(10)
@simulate_potential_fail(.001, 14.000, 0.1)
def read_ph_sensor():
    return round(random.uniform(0.001, 14.000), 3)

# Run the tests a few times
test_count = 10
functions_to_test = [read_thermometer, read_ph_sensor]
for function_to_test in functions_to_test:
    print(f"Testing {function_to_test.__name__}")
    for test_iterator in range(0, test_count):
        print(function_to_test())

## Print sensor timings 
print(f"Thermometer intervals: {read_thermometer.timings}")
print(f"pH sensor intervals: {read_ph_sensor.timings}")