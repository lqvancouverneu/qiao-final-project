from typing import List, Tuple
from src.graph import Graph


def dfs_pathfind(graph: Graph, start: str, goal: str) -> List[Tuple[List[str], float]]:
    stack = [(start, [start], 0)]
    all_routes = []
    
    while stack:
        current_node, path, cost = stack.pop()
        
        if current_node == goal:
            for i, city_id in enumerate(path):
                city_name = graph.nodes[city_id]['name']
                path[i] = city_name
            all_routes.append((path, cost))
            continue
        
        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor], cost + weight))
    
    return all_routes
