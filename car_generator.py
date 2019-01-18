# -*- coding: utf-8 -*-
import car, random

class CarGenerator:
    def __init__(self, graph, nr_of_cars):
        self.graph = graph
        self.nr_of_cars = nr_of_cars
        self.nodes = None
        self.generated_cars = []
        
    
    def __get_nodes_from_graph__(self):
        nodes = []
        for node in self.graph:
            nodes.append(node)
        self.nodes = nodes
    
    def generate_cars(self):
        self.__get_nodes_from_graph__()
        cars_generated = 0
        while cars_generated <= self.nr_of_cars:
            random_node = random.choice(self.nodes)
            new_car = car.Car(random_node)
            cars_generated += 1
            self.generated_cars.append(new_car)
            
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()

    
