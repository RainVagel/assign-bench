# -*- coding: utf-8 -*-

import click


@click.command("generate-graph") # TODO mõelda, mis käsud meil on mida saab jooksutada
@click.option("--vertices", help="Number of vertices.")
@click.option("--edges", help="Number of edges.")
@click.option("--max_weight", help="Max possible weight of an edge.")
#@click.option('', help='Number of greetings.')
#@click.option('--name', prompt='Your name',
#              help='The person to greet.')

@click.command()
def cli():
    click.echo("Hello World")

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

def main():
    pass

if __name__ == "__main__":
    main()