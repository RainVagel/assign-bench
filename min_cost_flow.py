from graph import dijkstra, node_id_to_node, read_graph
from car_generator import CarGenerator
from passenger import create_passenger


class MinCostFlowNetwork:
    def __init__(self, graph, cars, passengers):
        # Edges is a list of edges that consists of a tuple (car, passenger, distance, flow_unit)
        self.graph = graph
        self.cars = cars
        self.passengers = passengers
        self.edges = []
        self.passenger_id_to_passenger = self.create_passenger_id_to_passenger()

    def create_passenger_id_to_passenger(self):
        dictionary = {}
        for passenger in self.passengers:
            dictionary[passenger.id] = passenger
        return dictionary

    def __create_source(self):
        for car in self.cars:
            self.edges.append((-1, car, 0, 0))

    def __create_sink(self):
        for passenger in self.passengers:
            self.edges.append((passenger, -2, 0, 0))

    def populate(self):
        id_to_node = node_id_to_node(self.graph)
        passenger_ids = [passenger.id for passenger in self.passengers]
        # For every car I will calculate distances to every node
        for car in self.cars:
            # Get the distances and paths to every node from car location
            dist, prev = dijkstra(self.graph, id_to_node, car.location)
            # For every car I will create extra passengers that are connected to only that car. In the end,
            # all cars are connected to every passenger but any two cars are not connected to the exact same
            # passenger node
            for passenger_id in passenger_ids:
                self.edges.append((car, self.passenger_id_to_passenger[passenger_id], dist[passenger_id], 0))
        # Add source and sink to network
        self.__create_source()
        self.__create_sink()

    # Will be used to push flow through the network till it has maximum min-cost flow
    def push(self):
        pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def try_out():
    graph = read_graph("graph.json")
    car_generator = CarGenerator(graph, 2)
    passengers = [create_passenger(1, graph, 10), create_passenger(2, graph, 10), create_passenger(3, graph, 10)]
    car_generator.generate_cars()
    cars = car_generator.generated_cars
    network = MinCostFlowNetwork(graph, cars, passengers)
    network.populate()
    print(network.edges)


if __name__ == "__main__":
    try_out()

# https://cs.stackexchange.com/questions/33680/how-can-i-solve-this-constrained-assignment-problem
