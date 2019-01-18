from graph import read_graph
from car_generator import CarGenerator

class Passenger:

    def __init__(self, location, destination, wait_time):
        self.location = location
        self.destination = destination
        self.wait_time = wait_time

    def is_at_dest(self):
        if self.location == self.destination:
            return True
        return False


graph = read_graph("graph.json")
car_gen = CarGenerator(graph, 3)
car_gen.generate_cars()
print(car_gen.generated_cars)