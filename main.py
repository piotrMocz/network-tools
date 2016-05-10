import networkx as nx
import matplotlib.pyplot as plt
import random


# network configuration:
node_cnt = 100
focal_points = [1, 16, 50, 80, 99]  # np.random.choice(node_cnt, 5)
min_1_order_neighbours = 10
max_1_order_neighbours = 40
min_2_order_neighbours = 4
max_2_order_neighbours = 14
cluster_count = 5
min_intercluster_conns = 10
max_intercluster_conns = 20


def neighbours_1_cnt():
    global min_1_order_neighbours, max_1_order_neighbours
    return random.randrange(min_1_order_neighbours, max_1_order_neighbours)


def neighbours_2_cnt():
    global min_2_order_neighbours, max_2_order_neighbours
    return random.randrange(min_2_order_neighbours, max_2_order_neighbours)


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
    global cluster_count, min_intercluster_conns, max_intercluster_conns

    G = nx.Graph()

    # generate a forest of trees of order 2:
    roots = [make_random_2tree(G) for i in xrange(cluster_count)]

    # randomly connect the trees:
    ic_conns_cnt = random.randrange(min_intercluster_conns, max_intercluster_conns)
    for i in xrange(ic_conns_cnt):
        c1, c2 = random.sample(roots, 2)
        n1 = random_neighbour(G, c1)
        n2 = random_neighbour(G, c2)

        G.add_edge(n1, n2)

    return G


def export_graph(G, fname):
    with open(fname, 'w') as f:
        f.write(str(G.number_of_nodes()) + '\n')
        for e in G.edges():
            f.write(str(e[0]) + ' ' + str(e[1]) + '\n')


nodes = range(node_cnt)

G = nx.Graph()
G.add_nodes_from(nodes)

print G.nodes()
print focal_points
# print G.edges()

for fp in focal_points:
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
nx.draw(G)
# nx.draw_networkx_nodes(G, pos, nodelist=focal_points, node_size=800)
plt.show()
export_graph(G, 'graf.txt')
