import heapq
from typing import List, Tuple
from src.graph import Graph


def dijkstra_pathfind(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    queue = [(0, start, [start])]
    cost = {start: 0}
    
    while queue:
        current_cost, current_node, path = heapq.heappop(queue)
        
        if current_node == goal:
            for i, city_id in enumerate(path):
                city_name = graph.nodes[city_id]['name']
                path[i] = city_name
            return (path, current_cost)
        
        for neighbor, weight in graph.get_neighbors(current_node):
            new_cost = current_cost + weight
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))

    return ([], float('inf'))
