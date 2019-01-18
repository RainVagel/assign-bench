from graph import read_graph
from car_generator import CarGenerator

graph = read_graph("graph.json")
car_gen = CarGenerator(graph, 3)
car_gen.generate_cars()
print(car_gen.generated_cars)