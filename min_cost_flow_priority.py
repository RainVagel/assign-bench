from graph import dijkstra, node_id_to_node, read_graph
from car_generator import CarGenerator
from passenger import create_passenger, Passenger
from car import Car


class MinCostFlowPriorityNetwork:
    def __init__(self, graph, cars, passengers):
        # Edges is a list of edges that consists of a tuple (car, passenger, distance, flow_unit)
        self.graph = graph
        self.cars = cars
        self.passengers = passengers
        self.edges = []
        self.passenger_id_to_passenger = self.create_passenger_id_to_passenger()
        self.categories = self.__create_categories()

    # Creates category dictionary where each passenger is the key and the value is what category it is in.
    # Depending on the category, the distance will later be altered with the formula dist * category
    def __create_categories(self):
        categories = {}
        counter = 0
        category = 1
        while counter < len(self.passengers):
            categories[self.passengers[counter]] = category
            counter += 1
            if counter % len(self.cars) == 0:
                category += 1
        return categories

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

    # Will add the category weight to the distances between passengers and cars with the formula: dist * category
    def __add_category_weight(self):
        for edge in self.edges:
            if edge[1] in self.categories.keys():
                self.edges.remove(edge)
                edge = list(edge)
                edge[2] = edge[2] * self.categories[edge[1]] * 1.5
                edge = tuple(edge)
                self.edges.append(edge)

    # Creates adjacency list of edges.
    def __create_adj_list(self):
        self.adj_dict = {}
        for edge in self.edges:
            if edge[0] not in self.adj_dict:
                self.adj_dict[edge[0]] = [edge]
            else:
                self.adj_dict[edge[0]].append(edge)

    def __populate(self):
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
                self.edges.append((car, self.passenger_id_to_passenger[passenger_id],
                                   dist[self.passenger_id_to_passenger[passenger_id].starting_location.id_nr], 0))
        # Add source and sink to network
        # Will also add the category weights to the distances between cars and passengers.
        self.__add_category_weight()
        self.__create_source()
        self.__create_sink()
        self.__create_adj_list()

    def __push_modify_edges(self, node):
        # print("Push modify Node:", node)
        self.edges.remove(node)
        node = list(node)
        node[3] = 1
        node = tuple(node)
        self.edges.append(node)

    def __push_helper(self, node):
        # If the edge goes to the sink
        if node[1] == -2:
            # print("Sink")
            self.__push_modify_edges(node)
            return True
        else:
            sorted_adj = sorted(self.adj_dict[node[1]], key=lambda x: x[2])
            # print("Print sorted_adj", sorted_adj)
            for node_neighbour in sorted_adj:
                # print("Node_neighbour:", node_neighbour)
                if node_neighbour != node:
                    if node_neighbour[3] == 0:
                        # print("Agree")
                        if self.__push_helper(node_neighbour):
                            if node_neighbour[1] != -2:
                                self.__push_modify_edges(node_neighbour)
                            return True

    # Will be used to push flow through the network till it has maximum min-cost flow
    def __push(self):
        flows = 0
        for source_car in self.adj_dict[-1]:
            if source_car[3] == 0:
                if self.__push_helper(source_car):
                    self.__push_modify_edges(source_car)
                    self.__create_adj_list()
                    flows += 1

    def testing_network_printer(self):
        for key in self.adj_dict.keys():
            print(key)
            print("Goes to")
            print([(x[1], x[2], x[3]) for x in self.adj_dict[key]])

    def category_add_tester(self):
        self.__populate()
        print(self.edges)
        self.__add_category_weight()
        print(self.edges)

    # Returns array which consists of arrays with elements [car_id, passenger_id]
    def get_assignment(self):
        self.__populate()
        self.__push()
        assignment = []
        for key in self.adj_dict.keys():
            test_car = Car(0, 0, 0, 0)
            if type(key) == type(test_car):
                for passenger in self.adj_dict[key]:
                    # print(passenger)
                    if passenger[3] == 1:
                        assignment.append([passenger[0].id, passenger[1].id])
        return assignment

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def try_out():
    graph = read_graph("graph.json")
    car_generator = CarGenerator(graph)
    passengers = [create_passenger(1, graph, 10), create_passenger(2, graph, 10), create_passenger(3, graph, 10),
                  create_passenger(4, graph, 10)]
    car_generator.generate_cars(2)
    cars = car_generator.generated_cars
    network = MinCostFlowPriorityNetwork(graph, cars, passengers)
    # network.populate()
    # print(network.edges)
    # print(network.adj_dict[-1])
    # print(network.adj_dict)
    # network.push()
    # network.testing_network_printer()
    # print(network.get_assignment())
    # print(network.categories)
    network.category_add_tester()


if __name__ == "__main__":
    try_out()

# https://cs.stackexchange.com/questions/33680/how-can-i-solve-this-constrained-assignment-problem
# With added "categories" as priorities, where passengers are connected to categories such that the lower priority
# a passenger is, the higher the cost of picking him up.
