import graph as grp
from car_generator import CarGenerator
from passenger import create_passenger
import time

graph = grp.read_graph("graph.json")
node_id_node = grp.node_id_to_node(graph)
id_node = grp.node_to_node_id(graph)
    
    
car_gen = CarGenerator(graph)
generated_cars = car_gen.generate_cars(3, node_id_node, graph)

#print(car_gen.generated_cars)

# Generate a car and a passenger
test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
test_passenger = create_passenger(1, graph, 10)


while test_car.location != test_passenger.location:
    test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
    test_passenger = create_passenger(1, graph, 10)

print(car_gen.generated_cars)
print(test_passenger)

dist, prev = grp.dijkstra(graph, node_id_node, test_car.location, test_passenger.location)


# Car - go to passenger location
#test_car.set_path(path_to_passenger)
test_car.start_task(test_passenger)
print(list(reversed(test_car.path)))

test_car.movement()
# Testi, kui auto ja vend spawnivad samas kohas


def simulate(graph, nr_of_cars):
    car_generator = CarGenerator(graph)
    ticker = 0
    while ticker < 10000:
        pass