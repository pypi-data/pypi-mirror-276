# voyger.py

class rocket():
    def __init__(self, name :str, mass : int, velocity : int, thrust : int, show_static = False):
        self.name : str = name
        self.mass : int = mass 
        self.velocity : int = velocity
        self.thrust : int = thrust
        if show_static is not False:
            print("Name : ",rocket.name)
            print("Mass : ",rocket.mass)
            print("Velocity : ",rocket.velocity)
            print("Thrust : ",rocket.thrust)
            print("Show_Static : ",rocket.show_static)
    
        
        
voyger = rocket("voyger", 1000, 800, 30)


        
