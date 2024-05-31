import random 

class rocket():
    def __init__(self, name : str, mass : float, velocity : float, acceleration : float,
                 color : str = "White", fuel : int = 100000, speed : int = 100, fuel_type : str = "rocket fuel"):
        self.name = name
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration
        self.color = color
        self.fuel = fuel
        self.speed = speed
        self.fuel_type = fuel_type
        
        
        
my_rocket = rocket("Voyger", 1000.876, 900.97, 10.79, color="White", fuel= 1000000, speed=800, fuel_type="Nuclear Waste")    

