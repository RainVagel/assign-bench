import click
from graph import generate_graph as gg, output_graph
from simulator import start_simulate

@click.group()
def main():
    """TODO - lisada siia kirjeldus, mis programm teeb ja stuff
    """
    pass

@main.command(short_help="Generate your own graph by providing your own number of vertices, "
              + "edges and the maximum possible weight of an edge, e.g. "
              + "generate_graph 10 30 50")
@click.argument('args', nargs=3, type=int)
@click.option("--output_file", "-o", 
              help='Name of the output file without extension in which the generated graph will be saved.')

def generate_graph(args, output_file):
    """\bGenerate your own graph by providing your own number of vertices,
    edges and the maximum possible weight of an edge, e.g. generate_graph 10 30 50
    """
    vertices = args[0]
    edges = args[1]
    weight = args[2]
    graph = gg(vertices, edges, weight)
    if output_file:
        output_graph(graph, output_file)

#@main.command(short_help="Run a simulation (with a possibility of providing " +
#            "your own graph and algorithm) to find an average waiting time " + 
#            "for a passenger, number of passengers who got tired of waiting " +
#            "for a taxi and much more. Will also give visualizations to " + 
#            "better understand results.")
#@click.argument('args', nargs=2)
#@click.option("--input_file" , "-i", help="Name of the input graph file without " 
#              + "extension to be used to run the algorithms on.")
#@click.option("--algorithm", "-a", help="Name of the input algorithm file "
#              + "without extension. Algorithm must be a class, where __init__() "
#              + "must contain variables graph, number of cars and number of passengers, "
#              +"e.g. __init__(self, graph, cars, passengers).")
#@click.option("--test", "-t", nargs=2)
#def simulate(args, input_file, algorithm, test): # TODO
#    """\bRun a simulation with a given number of passengers (with a possibility
#    of providing your own graph and algorithm) to find an average waiting time
#    for a passenger, number of passengers who got tired of waiting for a taxi 
#    and much more. Will also give visualizations to better understand results. 
#    Examples: simulate 5, simulate 7 -i connected_graph -a hungarian_method
#    """
#    if test:
#        test_time(test[0], test[1])
        
@main.command(short_help="Run a simulation (with a possibility of providing " +
            "your own graph and algorithm) to find an average waiting time " + 
            "for a passenger, number of passengers who got tired of waiting " +
            "for a taxi and much more. Will also give visualizations to " + 
            "better understand results. Examples: simulate 5, simulate 7 -i " +
            "connected_graph -a hungarian_method HungarianMethod \"Hungarian Method\"")
@click.argument('nr_of_cars', nargs=1) 
@click.option("--input_file" , "-i", help="Name of the input graph file without " 
              + "extension to be used to run the algorithms on.")
@click.option("--algorithm", "-a", nargs=3, help="Name of the input algorithm file "
              + "without extension. Algorithm must be a class, where __init__() "
              + "must contain variables graph, number of cars and number of passengers, "
              + "e.g. __init__(self, graph, cars, passengers). Arguments are file name, "
              + "class name and algorith name to be displayed on the plots, e.g. "
              + "-a min_cost_flow MinCostFlowNetwork \"Minimum Cost Flow Network\"") # TODO lisa nimi ka siia
@click.option("--plot_name", "-p", help="Name of the algorithm to be displayed "
              + "on the plots.")
def simulate(nr_of_cars, input_file, algorithm, plot_name):
    """\bRun a simulation with a given number of passengers (with a possibility
    of providing your own graph and algorithm) to find an average waiting time
    for a passenger, number of passengers who got tired of waiting for a taxi 
    and much more. Will also give visualizations to better understand results. 
    Examples: simulate 5, simulate 7 -i connected_graph -a hungarian_method 
    HungarianMethod \"Hungarian Method\"
    """
    if algorithm:
        package = algorithm[0]
        name = algorithm[1]
        algo_name = algorithm[2]
        imported = getattr(__import__(package, fromlist=[name]), name)

    if input_file:
        if algorithm:
            start_simulate(nr_of_cars, input_file, imported, algo_name)
        else:
            start_simulate(nr_of_cars, input_file)
    elif algorithm:
        start_simulate(nr_of_cars, algorithm=imported, algorithm_name=algo_name)
    else:
        start_simulate(nr_of_cars)
    
if __name__ == '__main__':
    main()
    
