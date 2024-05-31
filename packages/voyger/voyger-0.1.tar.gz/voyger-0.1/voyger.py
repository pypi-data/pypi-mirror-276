# voyger.py

def greet():
    """Prints a greeting message."""
    print("Hello from Voyger!")


class Voyager:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        """Returns the name of the Voyager."""
        return self.name
