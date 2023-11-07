class Turtle():
    def __init__(self):
        self.health = 100
        self.max_temp = 100
        self.min_temp = 15
        self.temp = 20

    def report_health(self):
        return self.health    

    def update(self, aquarium):
        self.temp += ((aquarium.water_temperature - self.temp) * 0.9) 

class Aquarium:
    def __init__(self):
        self.water_temperature = 10
        self.ph = 5.5
        self.turtle = Turtle()


class Plant:
    def __init__(self):
        self.room_temperature = 15
        self.aquarium = Aquarium()


plant = Plant()
while True:
    plant.aquarium.turtle.update(aquarium)
    print("Turtle Health:", plant.aquarium.turtle.report_health())