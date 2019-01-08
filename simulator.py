class Passenger:

    def __init__(self, location, destination, wait_time):
        self.location = location
        self.destination = destination
        self.wait_time = wait_time

    def is_at_dest(self):
        if self.location == self.destination:
            return True
        return False
