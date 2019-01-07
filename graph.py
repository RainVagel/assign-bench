import random


class Node:
    def __init__(self, id_nr):
        self.id_nr = id_nr
        self.passengers = 0
        self.adj_list = []

    def has_passengers(self):
        if self.passengers > 0:
            return True
        return False

    def create_passenger(self):
        self.passengers += 1

    def add_edge(self, other, weight):
        self.adj_list.append((other, weight))

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def random_add_edges(graph, edges, max_weight):
    while edges > 0:
        index_1 = random.randint(0, len(graph) - 1)
        index_2 = random.randint(0, len(graph) - 1)
        while index_2 == index_1:
            index_2 = random.randint(0, len(graph) - 1)
        weight = random.randint(1, max_weight)
        graph[index_1].add_edge(graph[index_2], weight)
        graph[index_2].add_edge(graph[index_1], weight)
        edges -= 1
    return graph


def generate_graph(vertices, edges, max_weight):
    current_id = 0
    graph = set()

    # Create all the vertices of the graph
    for i in range(vertices):
        graph.add(Node(current_id))
        current_id += 1

    # Generate a spanning tree
    S, T = graph, set()
    current_node = random.sample(S, 1).pop()
    S.remove(current_node)
    T.add(current_node)
    while S:
        new_node = random.sample(S, 1).pop()
        S.remove(new_node)
        weight = random.randint(1, max_weight)
        current_node.add_edge(new_node, weight)
        new_node.add_edge(current_node, weight)
        T.add(new_node)
        current_node = new_node

    edges = edges - (vertices - 1)
    graph = list(T)

    return random_add_edges(graph, edges, max_weight)


def main():
    print(generate_graph(5, 10, 20))


if __name__ == "__main__":
    main()
