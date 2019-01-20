import click
from graph import generate_graph as gg, output_graph

@click.group()
def main():
    """TODO - lisada siia kirjeldus, mis programm teeb ja stuff
    """
    pass

@main.command(short_help="Generate your own graph by providing your own number of vertices, "
              + "edges and the maximum possible weight of an edge, e.g. "
              + "generate_graph 10 30 50")
@click.argument('args', nargs=3, type=int)
@click.option("--output_file", 
              help='Name of the output file in which the generated graph will be saved.')

def generate_graph(args, output_file):
    """\bGenerate your own graph by providing your own number of vertices,
    edges and the maximum possible weight of an edge, e.g. generate_graph 10 30 50
    """
    vertices = args[0]
    edges = args[1]
    weight = args[2]
    graph = gg(vertices, edges, weight)
    #click.echo(graph)
    if output_file:
        output_graph(graph, output_file)
@main.command(short_help="Run a simulation with an assigned algorithm to find "
              + "an average waiting time for a passenger, TODO")
@click.argument('args', nargs=2)
# TODO - lisa option, et lisada enda algoritm, enda graaf, 
def simulate(args):
    """\bRun a simulation with an assigned algorithm to find an average 
    waiting time for a passenger, TODO
    """
    click.echo(args)

if __name__ == '__main__':
    main()