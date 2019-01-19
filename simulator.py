from graph import read_graph
from car_generator import CarGenerator
from passenger import create_passenger

graph = read_graph("graph.json")
car_gen = CarGenerator(graph)
car_gen.generate_cars(3)
#print(car_gen.generated_cars)

# Generate a car and a passenger
test_car = car_gen.generate_cars(1)[0]
test_passenger = create_passenger(graph, 10)


while test_car.location == test_passenger.location:
    test_car = car_gen.generate_cars(1)[0]
    test_passenger = create_passenger(graph, 10)

print(car_gen.generated_cars)
print(test_passenger)