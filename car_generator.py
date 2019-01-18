# -*- coding: utf-8 -*-
import car, random, itertools

class CarGenerator:
    id_generator = itertools.count()
    def __init__(self, graph):
        self.graph = graph
        self.nr_of_cars = 0
        self.nodes = self.__get_nodes_from_graph__()
        self.generated_cars = []
        
    
    def __get_nodes_from_graph__(self):
        nodes = []
        for node in self.graph:
            nodes.append(node.id_nr)
        return nodes
    
    def generate_cars(self, nr):
        generated_cars = []
        cars_generated = 0
        while cars_generated < nr:
            new_id = next(self.id_generator)
            random_node = random.choice(self.nodes)
            new_car = car.Car(random_node, new_id)
            cars_generated += 1
            generated_cars.append(new_car)
        self.generated_cars = generated_cars
        self.nr_of_cars = cars_generated
        return generated_cars
    
    def add_new_cars(self, nr):
        generated_cars = []
        cars_generated = 0
        while cars_generated < nr:
            new_id = next(self.id_generator)
            random_node = random.choice(self.nodes)
            new_car = car.Car(random_node, new_id)
            cars_generated += 1
            generated_cars.append(new_car)
        self.generated_cars.extend(generated_cars)
        self.nr_of_cars += cars_generated
        return self.generated_cars
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()

    
