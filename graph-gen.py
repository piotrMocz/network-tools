import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from time import time
from string import strip
from config import Config

FOCAL_POINTS = [1, 8, 16, 32, 50, 64, 700, 800, 4311, 7123, 9900]  # np.random.choice(node_cnt, 5)
config = Config(FOCAL_POINTS)


def neighbours_1_cnt():
    global config
    return random.randrange(config.min_1_order_neighbours,
                            config.max_1_order_neighbours)


def neighbours_2_cnt():
    global config
    return random.randrange(config.min_2_order_neighbours,
                            config.max_2_order_neighbours)


def make_random_2tree(G):
    # root of the 2-tree:
    root = random.choice(G.nodes())

    # neighbours of order 1:
    n1_cnt = neighbours_1_cnt()
    for i in xrange(n1_cnt):
        n1 = random.choice(G.nodes())
        G.add_edge(root, n1)

        # neighbours of order 2:
        n2_cnt = neighbours_2_cnt()
        for j in xrange(n2_cnt):
            n2 = random.choice(G.nodes())
            G.add_edge(n1, n2)

    return root


def random_neighbour(G, root):
    if random.random() < 0.05:
        return root

    n1 = random.choice(G.neighbors(root))
    if random.random() < 0.25:
        return n1

    return random.choice(G.neighbors(n1))


def random_net():
    """
    Creates a networkx graph representing a social network graph.
    :return: networkx Graph object
    """
    print "Creating a random network..."
    t_start = time()
    global config

    G = nx.Graph()

    # generate a forest of trees of order 2:
    roots = [make_random_2tree(G) for i in xrange(config.cluster_count)]

    # randomly connect the trees:
    ic_conns_cnt = random.randrange(config.min_intercluster_conns,
                                    config.max_intercluster_conns)
    for i in xrange(ic_conns_cnt):
        c1, c2 = random.sample(roots, 2)
        n1 = random_neighbour(G, c1)
        n2 = random_neighbour(G, c2)

        G.add_edge(n1, n2)

    t_elapsed = time() - t_start
    print "Finished! Time elapsed: {0}".format(t_elapsed)
    return G


def import_graph(fname):
    """
    Imports graph from a file.
    :param fname: File to read the graph from.
    :return: networkx Graph object
    """
    with open(fname, 'r') as f:
        G = nx.Graph()

        V = int(strip(f.readline()))

        for i in xrange(V):
            line = strip(f.readline())
            v1, v2 = map(int, line.split(' '))
            G.add_edge(v1, v2)

        return G


def export_graph(G, fname):
    """
    Exports a networkx Graph to file.
    Format:
    number_of_vertices
    [subsequent edges]
    :param G: networkx Graph
    :param fname: File to dump the graph to
    :return: void
    """
    with open(fname, 'w') as f:
        f.write(str(G.number_of_nodes()) + '\n')
        for e in G.edges():
            f.write(str(e[0]) + ' ' + str(e[1]) + '\n')


def graph_histogram(G, bins=None):
    print "Plotting friend count histogram..."
    t_start = time()

    V = len(G.nodes())
    ys = np.zeros(V)
    bin_cnt = V / 10 if bins is None else bins

    for idx, v in enumerate(G.nodes()):
        ys[idx] = len(G.neighbors(v))

    # ys = filter(lambda x: x > 0, ys)
    # ys = np.log10(ys)
    # ys = filter(lambda x: x > 0, ys)
    # ys = np.log10(ys)

    plt.hist(ys, bins=bin_cnt)
    plt.ylabel('Number of users with given friend count')
    plt.title('Histogram of frienship counts per user')
    plt.plot()
    plt.savefig('friend-histogram.png')
    plt.close()

    t_elapsed = time() - t_start
    print "Finished! Time elapsed: {0}".format(t_elapsed)


def generate_graph(plot_graph=False, plot_histogram=False):
    global config
    nodes = range(config.node_cnt)

    G = nx.Graph()
    G.add_nodes_from(nodes)

    # print G.nodes()
    print config.focal_points
    # print G.edges()

    for fp in config.focal_points:
        # select a random number of neighbours for the focal point:
        num_neighbours = random.randrange(10, 150)
        neighbours = [random.choice(nodes) for i in xrange(num_neighbours)]
        for n in neighbours:
            G.add_edge(fp, n)

    for node in nodes:
        # select a random number of neighbours for the focal point:
        num_neighbours = random.randrange(2, 3)
        neighbours = [random.choice(nodes) for i in xrange(num_neighbours)]
        for n in neighbours:
            G.add_edge(node, n)

    # pos = nx.spectral_layout(G)
    if plot_graph:
        nx.draw(G)
        # nx.draw_networkx_nodes(G, pos, nodelist=focal_points, node_size=800)
        plt.show()

    if plot_histogram:
        graph_histogram(G, bins=len(G.nodes()))

    export_graph(G, 'graf.txt')


if __name__ == '__main__':
    generate_graph()
    G = import_graph('graf.txt')
    graph_histogram(G)
