from collections import deque
from typing import List, Tuple
from src.graph import Graph


def bfs_pathfind(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    queue = deque([(start, [start], 0)])
    previous_level = {start}

    while queue:
        current_node, path, cost = queue.popleft()
        
        if current_node == goal:
            for i, city_id in enumerate(path):
                city_name = graph.nodes[city_id]['name']
                path[i] = city_name
            return (path, cost)
        
        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor not in previous_level:
                queue.append((neighbor, path + [neighbor], cost + weight))
                previous_level.add(neighbor)

    return ([], float('inf'))
