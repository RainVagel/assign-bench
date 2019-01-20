import random
import json
import numpy as np


class Node:
    def __init__(self, id_nr):
        self.id_nr = id_nr
        # Array of passenger objects
        self.passengers = []
        # adj list consists of arrays [neighbour_id, dist_to_neighbour]
        self.adj_list = []

    def add_passenger(self, passenger):
        # print(self.passengers)
        self.passengers.append(passenger)

    def has_passengers(self):
        if len(self.passengers) > 0:
            return True
        return False

    def add_edge(self, other, weight):
        self.adj_list.append((other, weight))

    def is_edge_adj(self, other):
        nodes = set()
        for edge in self.adj_list:
            nodes.add(edge[0])
        if other in nodes:
            return True
        return False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.id_nr)


def count_edges(graph):
    edges = []
    for node in graph:
        for edge in node.adj_list:
            edges.append(edge)
    return len(edges) / 2


def random_add_edges(graph, edges, max_weight):
    while edges > 0:
        index_1 = random.randint(0, len(graph) - 1)
        index_2 = random.randint(0, len(graph) - 1)
        while index_2 == index_1 or graph[index_1].is_edge_adj(graph[index_2].id_nr):
            index_1 = random.randint(0, len(graph) - 1)
            index_2 = random.randint(0, len(graph) - 1)
        weight = random.randint(1, max_weight)
        graph[index_1].add_edge(graph[index_2].id_nr, weight)
        graph[index_2].add_edge(graph[index_1].id_nr, weight)
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
        current_node.add_edge(new_node.id_nr, weight)
        new_node.add_edge(current_node.id_nr, weight)
        T.add(new_node)
        current_node = new_node

    edges = edges - (vertices - 1)
    graph = list(T)

    return random_add_edges(graph, edges, max_weight)


def output_graph(graph):
    dictionary = {}
    for node in graph:
        dictionary[node.id_nr] = {"id": node.id_nr, "passengers": node.passengers,
                                  "adj_list": node.adj_list}
    with open("graph.json", "w") as write_file:
        json.dump(dictionary, write_file)


def dict_to_array(graph_dictionary):
    graph = []
    for key in graph_dictionary.keys():
        id_nr = graph_dictionary[key]["id"]
        passengers = graph_dictionary[key]["passengers"]
        adj_list = graph_dictionary[key]["adj_list"]
        node = Node(id_nr=id_nr)
        node.passengers = passengers
        node.adj_list = adj_list
        graph.append(node)
    return graph


def read_graph(path_file):
    with open(path_file) as data_file:
        data_loaded = json.load(data_file)
    return dict_to_array(data_loaded)


def node_amount(vertices, edges):
    if edges > vertices*(vertices-1)/2:
        raise ValueError("Number of edges can not exceed nr_vertices(nr_vertices-1)/2")
    elif edges < vertices - 1:
        raise ValueError("Number of edges can not be smaller than nr_vertices-1")
    elif vertices < 2:
        raise ValueError("Number of vertices can not be less than 2")


def validate(vertices, edges):
    try:
        node_amount(vertices, edges)
    except ValueError as e:
        print("Caught error:", repr(e))


def key_value(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    index = 0
    final_array = []
    while index < len(keys):
        final_array.append((keys[index], values[index]))
        index += 1
    return final_array


"""
:param source - Node, where the taxi is
:param id_to_node - ID to node dictionary
:target - Node, where the passenger is
"""


def dijkstra(graph, id_to_node, source, target=None):
    vertex_set = set()

    dist = {}
    prev = {}

    for node in graph:
        dist[node.id_nr] = np.inf
        prev[node.id_nr] = None
        vertex_set.add(node)

    dist[source.id_nr] = 0

    while vertex_set:
        key_value_array = key_value(dist)
        # u is Node
        key_value_array = sorted(key_value_array, key=lambda t: t[1])
        u = key_value_array[0][0]
        index = 0
        while id_to_node[u] not in vertex_set:
            u = key_value_array[index][0]
            index += 1
        vertex_set.remove(id_to_node[u])

        if target is not None:
            if u == target.id_nr:
                return dist, prev

        # Neighbour is array [neighbour_id, dist_to_neighbour]
        for neighbour in id_to_node[u].adj_list:
            if id_to_node[neighbour[0]] in vertex_set:
                alt = dist[u] + neighbour[1]
                if alt < dist[neighbour[0]]:
                    dist[neighbour[0]] = alt
                    # prev[neighbour[0]].append(u)
                    prev[neighbour[0]] = u
    return dist, prev


"""
:param graph - Array of graph nodes.
:returns dictionary - Keys node_id, values nodes
"""


def node_id_to_node(graph):
    graph_dict = {}
    for node in graph:
        graph_dict[node.id_nr] = node
    return graph_dict


def node_to_node_id(graph):
    graph_dict = {}
    for node in graph:
        graph_dict[node] = node.id_nr
    return graph_dict


def path_to_target(prev, id_to_node, source, target):
    s = []
    u = target
    if prev[u.id_nr] is not None or u == source.id_nr:
        while u is not None:
            s.insert(0, u)
            if prev[u.id_nr] is None:
                break
            else:
                u = id_to_node[prev[u.id_nr]]
    return [x.id_nr for x in s][1:]


def generate_nn_matrix(graph):
    dist = []
    for node in graph:
        temp = []
        for node in graph:
            temp.append(node)
        dist.append(temp)
    return dist


# Returns list of tuples with elements (u_id, v_id, weight) which is the edge from u to v and with edge weight
def get_edges(graph):
    edges = []
    for node in graph:
        for neighbour in node.adj_list:
            edges.append((node.id_nr, neighbour[0], neighbour[1]))
    return edges


def floyd_warshall(graph):
    # Generate the dist matrix with inf elements
    dist = []
    for node in graph:
        temp = []
        for node in graph:
            temp.append(np.inf)
        dist.append(temp)

    for edge in get_edges(graph):
        dist[edge[0]][edge[1]] = edge[2]

    for node in graph:
        dist[node.id_nr][node.id_nr] = 0

    for k in range(0, len(graph)):
        for i in range(0, len(graph)):
            for j in range(0, len(graph)):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def get_diameter(graph):
    distances = floyd_warshall(graph)
    maximum = 0
    for row in distances:
        maximum = max(maximum, max(row))
    return maximum


def main():
    # output_graph(generate_graph(200, 15000, 200))
    graph = read_graph("graph.json")
    print(get_diameter(graph))
    node_id_node = node_id_to_node(graph)
    # id_node = node_to_node_id(graph)
    dist, prev = dijkstra(graph, node_id_node, graph[0], graph[-1])
    print(graph)
    print(dist)
    print("Prev", prev)
    print(path_to_target(prev, node_id_node, graph[0], graph[-1]))


if __name__ == "__main__":
    main()
