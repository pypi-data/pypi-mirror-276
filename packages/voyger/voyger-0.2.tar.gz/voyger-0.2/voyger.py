# voyger.py

class rocket():
    def __init__(self, name :str, mass : int, velocity : int, thrust : int):
        self.name : str = name
        self.mass : int = mass 
        self.velocity : int = velocity
        self.thrust : int = thrust
        
    def rocket_state(rocket : any):
        print("Name : ",rocket.name)
        print("Mass : ",rocket.mass)
        print("Velocity : ",rocket.velocity)
        print("Thrust : ",rocket.thrust)
        
        
voyger = rocket("voyger", 1000, 800, 30)
rocket.rocket_state(voyger)

        
