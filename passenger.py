from random import choice
from graph import *

# Time interval on how often a passenger is created
PASSENGER_INTERVAL = 10


class Passenger:

    def __init__(self, id, starting_location, destination, wait_time):
        self.id = id
        self.starting_location = starting_location
        self.location = starting_location
        self.destination = destination
        self.wait_time = wait_time
        self.on_car = False
        self.time_waited = 0

    def time_movement(self):
        if self.on_car is False:
            self.wait_time -=1
            self.time_waited += 1
            if self.wait_time == 0:
                return True
            else:
                return False
        else:
            return False

    def is_at_dest(self):
        if self.location == self.destination:
            return True
        return False
    
    def set_location(self, node):
        self.location = node
    
    def set_on_car(self, boolean):
        self.on_car = boolean
    
    def __set_node__(self, node_ids):
        return node_ids[self.location]

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


def main():
    graph = read_graph("graph.json")
    # passengers = [create_passenger(graph, 10), create_passenger(graph, 10)]
    # for node in graph:
    #     if len(node.passengers) > 0:
    #         print(node.passengers[0])
    #     print(node)
    # print(passengers)


if __name__ == "__main__":
    main()