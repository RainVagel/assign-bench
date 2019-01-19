import graph as grp
from car_generator import CarGenerator
from passenger import create_passenger
import time

PASSENGER_INTERVAL = 10

graph = grp.read_graph("graph.json")
node_id_node = grp.node_id_to_node(graph)
id_node = grp.node_to_node_id(graph)
    
    
car_gen = CarGenerator(graph)
generated_cars = car_gen.generate_cars(3, node_id_node, graph)

#print(car_gen.generated_cars)

# Generate a car and a passenger
test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
test_passenger = create_passenger(1, graph, 10)


while test_car.location == test_passenger.location:
    test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
    test_passenger = create_passenger(1, graph, 10)

print(car_gen.generated_cars)
print(test_passenger)

dist, prev = grp.dijkstra(graph, node_id_node, test_car.location, test_passenger.location)

path_to_destination = grp.path_to_target(prev, test_passenger.location)
# Car - go to passenger location
#test_car.set_path(path_to_passenger)
test_car.start_task(test_passenger)
print(list(reversed(test_car.path)))

test_car.movement()
# Testi, kui auto ja vend spawnivad samas kohas

def simulate(input_graph, nr_of_cars, nr_of_passengers):
    # Replace hard-coded string with input graph
    graph = grp.read_graph("graph.json")
    node_id_node = grp.node_id_to_node(graph)
    id_node = grp.node_to_node_id(graph)
    
    free_cars = []
    driving_cars = []
    waiting_passengers = []
    picked_up_passengers = []
    
    car_generator = CarGenerator(graph)
    generated_cars = car_gen.generate_cars(nr_of_cars, node_id_node, graph)
    
    free_cars.extend(generated_cars)
    
    global PASSENGER_INTERVAL
    diam = grp.get_diameter(graph)
    counter_passenger = 0
    passenger_id = 0
    # while True is only for testing purpouses. Eventually will be handled by SimulatorManager
    while True:
        if counter_passenger % PASSENGER_INTERVAL == 0:
            waiting_passengers.append(create_passenger(passenger_id, graph, diam))
            passenger_id += 1
        # After every 100 passengers created, increase the speed at which new passengers are created
        if len(passenger_id) % 100 == 0:
            PASSENGER_INTERVAL -= 1
        counter_passenger += 1
    
    #gene