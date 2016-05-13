
class Config(object):
    def __init__(self, focal_points,
                 node_cnt=1000,
                 min_1_order_neighbours=10,
                 max_1_order_neighbours=40,
                 min_2_order_neighbours=4,
                 max_2_order_neighbours=14,
                 cluster_count=5,
                 min_intercluster_conns=10,
                 max_intercluster_conns=20):
        self.node_cnt = node_cnt
        self.focal_points = focal_points
        self.min_1_order_neighbours = min_1_order_neighbours
        self.max_1_order_neighbours = max_1_order_neighbours
        self.min_2_order_neighbours = min_2_order_neighbours
        self.max_2_order_neighbours = max_2_order_neighbours
        self.cluster_count = cluster_count
        self.min_intercluster_conns = min_intercluster_conns
        self.max_intercluster_conns = max_intercluster_conns
