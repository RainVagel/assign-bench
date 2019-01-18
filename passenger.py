from random import choice
from graph import *

PASSENGER_INTERVAL = 10


class Passenger:

    def __init__(self, location, destination, wait_time):
        self.location = location
        self.destination = destination
        self.wait_time = wait_time

    def is_at_dest(self):
        if self.location == self.destination:
            return True
        return False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()


def create_passenger(graph, passenger_wait_time):
    location = choice(graph)
    destination = choice(graph)

    # Keep randomly choosing destination until it is not the same as location
    while location == destination:
        destination = choice(graph)

    passenger = Passenger(location, destination, passenger_wait_time)
    location.add_passenger(passenger)

    return passenger


def main():
    graph = read_graph("graph.json")
    passengers = [create_passenger(graph, 10), create_passenger(graph, 10)]
    for node in graph:
        if len(node.passengers) > 0:
            print(node.passengers[0])
        print(node)
    print(passengers)


if __name__ == "__main__":
    main()