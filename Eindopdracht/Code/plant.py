import time, math
import random 
# Settings
temperature_damping_factor = 0.1
temperature_decimals = 2
max_room_temperature_change=2
room_temperature_change_chance = 2
max_room_temperature = 40
min_room_temperature = 10

class Turtle():
    def __init__(self):
        self.health = 100
        self.max_temp = 28
        self.min_temp = 22
        self.min_ph = 6.4
        self.max_ph = 7.6
        self.temp = 25
        self.isDead = False

    def report_health(self):
        return self.health          
    
    def report_temps(self):
        global temperature_decimals
        return round(self.temp, temperature_decimals)
    
    def update_health(self, aquarium):
        # Define a lambda function to calculate health decrement
        health_decrement = lambda temp_diff: math.pow(temp_diff, 2)

        # Calculate if temperature damage is needed
        temp_diff = 0
        if self.temp < self.min_temp:
            temp_diff = self.min_temp - self.temp
        elif self.temp > self.max_temp:
            temp_diff = self.temp - self.max_temp

        if temp_diff != 0:
            self.health -= health_decrement(temp_diff)
            self.health = max(self.health, 0)  # Ensure health doesn't go below 0
        
        # Calculate if ph damage is needed
        if aquarium.ph < self.min_ph or aquarium.ph > self.max_ph:
            self.health -= 10

        if self.health <= 0:
            self.health = 0
            self.isDead=True
        
    def update_temps(self, aquarium):
        global temperature_damping_factor
        # Change turtle temperature
        self.temp += (aquarium.water_temperature - self.temp) * temperature_damping_factor


    def update(self, aquarium):
        global temperature_damping_factor
        global temperature_decimals

        # Update turtle temperature
        self.update_temps(aquarium)
        # Update turtle health 
        self.update_health(aquarium)



class Aquarium:
    def __init__(self):
        self.water_temperature = 25
        self.ph = 7.0
        self.turtle = Turtle()

    def report_temps(self):
        global temperature_decimals
        return round(self.water_temperature, temperature_decimals)
    
    def report_ph(self):
        return self.ph    

    def update_temps(self, plant, simulated_heater, simulated_cooler):
        global temperature_damping_factor

        # Change aquarium temperature
        tempChange=0
        if simulated_heater.getState():
            tempChange+=1
        if simulated_cooler.getState():
            tempChange-=1

        if tempChange != 0:
            self.water_temperature+=tempChange
        else:
            self.water_temperature += (plant.room_temperature - self.water_temperature) * temperature_damping_factor
    
    def update_ph(self, simulated_ph_plus_pump, simulated_ph_min_pump):
        # Change aquarium temperature
        pHChange=0
        if simulated_ph_plus_pump.getState():
            pHChange+=0.1
        if simulated_ph_min_pump.getState():
            pHChange-=0.1

        if pHChange != 0:
            self.ph+=pHChange
        else:
            self.ph += random.randint(-1, 1)/10



    def update(self, plant, simulated_heater, simulated_cooler, simulated_ph_plus_pump, simulated_ph_min_pump):
        # Update turtle temperature
        self.update_temps(plant, simulated_heater, simulated_cooler)

        # Update ph 
        self.update_ph(simulated_ph_plus_pump, simulated_ph_min_pump)


class Plant:
    def __init__(self):
        self.room_temperature = 30
        self.aquarium = Aquarium()

    def update(self):
        global max_room_temperature_change
        global room_temperature_change_chance
        global max_room_temperature
        global min_room_temperature
        if(random.randint(0, 100) > 100-room_temperature_change_chance):
            self.room_temperature += round(random.randint(-max_room_temperature_change*10,max_room_temperature_change*10)/10, 2)
            # Clamp room temp to be 'realistic'something
            self.room_temperature = max(self.room_temperature, min_room_temperature)
            self.room_temperature = min(self.room_temperature, max_room_temperature)


class Simulator:
    def __init__(self):
        self.deaths = []
        self.plant = Plant()
        self.iteration=1

    def runIteration(self, simulated_heater, simulated_cooler, simulated_ph_plus_pump, simulated_ph_min_pump):
        self.plant.update()
        self.plant.aquarium.turtle.update(self.plant.aquarium)
        self.plant.aquarium.update(self.plant, simulated_heater, simulated_cooler, simulated_ph_plus_pump, simulated_ph_min_pump)

        print("--- Results For Iteration {} (Minutes) ---".format(self.iteration))
        print("Turtle Health:", self.plant.aquarium.turtle.report_health())
        print("Turtle Body Temperature:", self.plant.aquarium.turtle.report_temps())
        print("Aquarium Temperature:", self.plant.aquarium.report_temps())
        print("Aquarium pH:", self.plant.aquarium.report_ph())
        print("Target Room Temperature:", self.plant.room_temperature)
        print()

        if self.plant.aquarium.turtle.isDead:
            print("x_x at {} iterations".format(self.iteration))
            time.sleep(6000)

        self.iteration+=1


