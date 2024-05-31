class Rocket:
    """
    A class to represent a rocket.

    Attributes
    ----------
    name : str
        The name of the rocket.
    mass : float
        The mass of the rocket.
    velocity : float
        The current velocity of the rocket.
    acceleration : float
        The current acceleration of the rocket.
    color : str
        The color of the rocket.
    fuel : int
        The amount of fuel in the rocket.
    speed : int
        The speed of the rocket.
    fuel_type : str
        The type of fuel used by the rocket.
    """
    
    def __init__(self, name: str, mass: float, velocity: float, acceleration: float,
                 color: str = "White", fuel: int = 100000, speed: int = 100, fuel_type: str = "rocket fuel"):
        self.name = name
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration
        self.color = color
        self.fuel = fuel
        self.speed = speed
        self.fuel_type = fuel_type

    def start_rocket(self) -> None:
        """Print a message indicating that the rocket is started and ready to launch."""
        print("The Rocket is started and ready to launch.")
    
    def update_velocity(self, time: float) -> None:
        """Update the velocity based on acceleration and time."""
        self.velocity += self.acceleration * time
        print(f"Updated velocity: {self.velocity} m/s")
    
    def burn_fuel(self, amount: int) -> None:
        """Burn a specified amount of fuel."""
        if amount > self.fuel:
            print("Not enough fuel to burn.")
        else:
            self.fuel -= amount
            print(f"Burned {amount} units of fuel. Remaining fuel: {self.fuel}")
    
    def check_fuel_level(self) -> int:
        """Check the current fuel level."""
        print(f"Current fuel level: {self.fuel}")
        return self.fuel

    def __str__(self) -> str:
        """Return a string representation of the rocket."""
        return (f"Rocket(name={self.name}, mass={self.mass}, velocity={self.velocity}, "
                f"acceleration={self.acceleration}, color={self.color}, fuel={self.fuel}, "
                f"speed={self.speed}, fuel_type={self.fuel_type})")

# Example of creating a Rocket instance and using its methods
rocket = Rocket(name="Apollo", mass=5000.0, velocity=0.0, acceleration=9.8)
print(rocket)
rocket.start_rocket()
rocket.update_velocity(10)  # Update velocity after 10 seconds
rocket.burn_fuel(500)
rocket.check_fuel_level()
