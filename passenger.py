from random import choice
from graph import *

# Time interval on how often a passenger is created
PASSENGER_INTERVAL = 10


class Passenger:

    def __init__(self, id, location, destination, wait_time):
        self.id = id
        self.location = location
        self.destination = destination
        self.wait_time = wait_time
        self.on_car = False

    def is_at_dest(self):
        if self.location == self.destination:
            return True
        return False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()


def create_passenger(passenger_id, graph, passenger_wait_time):
    location = choice(graph)
    destination = choice(graph)

    # Keep randomly choosing destination until it is not the same as location
    while location == destination:
        destination = choice(graph)

    passenger = Passenger(passenger_id, location, destination, passenger_wait_time)
    location.add_passenger(passenger)

    return passenger


def passenger_generator(graph):
    global PASSENGER_INTERVAL
    diam = get_diameter(graph)
    counter = 0
    passenger_id = 0
    passengers = []
    # while True is only for testing purpouses. Eventually will be handled by SimulatorManager
    while True:
        if counter % PASSENGER_INTERVAL == 0:
            passengers.append(create_passenger(passenger_id, graph, diam))
            passenger_id += 1
        # After every 100 passengers created, increase the speed at which new passengers are created
        if len(passengers) % 100 == 0:
            PASSENGER_INTERVAL -= 1
        counter += 1


def main():
    graph = read_graph("graph.json")
    passenger_generator(graph)
    # passengers = [create_passenger(graph, 10), create_passenger(graph, 10)]
    # for node in graph:
    #     if len(node.passengers) > 0:
    #         print(node.passengers[0])
    #     print(node)
    # print(passengers)


if __name__ == "__main__":
    main()