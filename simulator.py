import graph as grp
from car_generator import CarGenerator
from passenger import create_passenger
import time

graph = grp.read_graph("graph.json")
car_gen = CarGenerator(graph)
car_gen.generate_cars(3)

#print(car_gen.generated_cars)

# Generate a car and a passenger
test_car = car_gen.generate_cars(1)[0]
test_passenger = create_passenger(1, graph, 10)


while test_car.location == test_passenger.location:
    test_car = car_gen.generate_cars(1)[0]
    test_passenger = create_passenger(1, graph, 10)

print(car_gen.generated_cars)
print(test_passenger)

node_id_node = grp.node_id_to_node(graph)
id_node = grp.node_to_node_id(graph)
dist, prev = grp.dijkstra(graph, node_id_node, graph[0], graph[-1])

# Car - go to passenger location
passenger_location = test_passenger.location.id_nr
path_to_passenger = prev[passenger_location]
test_car.path = path_to_passenger

test_car.movement()