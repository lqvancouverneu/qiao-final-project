from typing import List, Tuple


class Graph:
    def __init__(self):
        self.nodes = {
            # node_id1: {'name': city name1},
            # node_id2: {'name': city name2},
            # ...
        }
        self.edges = {
            # node_id1: [(to_node1, weight1), (to_node2, weight2), ...],
            # node_id2: [(to_node3, weight3), (to_node4, weight4), ...],
            # ...
        }
    
    def add_node(self, node_id: str, name: str):
        self.nodes[node_id] = {'name': name}
        self.edges[node_id] = []
    
    def add_edge(self, from_node: str, to_node: str, weight: float):
        self.edges[from_node].append((to_node, weight))
    
    def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        neighbors = self.edges.get(node_id)
        return neighbors
