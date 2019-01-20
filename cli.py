# -*- coding: utf-8 -*-

import click


@click.command() # TODO mõelda, mis käsud meil on mida saab jooksutada
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')

def run(): # TODO
    pass

class Test:
    
    def __init__(self, n):
        self.value = n
    
    def substract(self, x):
        self.value = self.value - x
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()
        
test = Test(15)
dick = {}
dick[1] = test
test.substract(3)