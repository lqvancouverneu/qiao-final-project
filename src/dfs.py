from typing import List, Tuple
from src.graph import Graph


def dfs_pathfind(graph: Graph, start: str, goal: str) -> Tuple[List[dict], List[Tuple[List[str], float]]]:
    """
    Performs Depth-First Search to find ALL possible routes from start to goal.
    
    Args:
        graph (Graph): The flight graph containing cities and routes
        start (str): Starting city ID (e.g., 'vancouver')
        goal (str): Destination city ID (e.g., 'new_york')
    
    Returns:
        Tuple[List[Dict], List[Tuple]]:     
            - steps: List of step-by-step actions for users to see the DFS process
            - all_routes: List of tuples containing (path, cost) for each route found
    
    Example:
        steps, all_routes = dfs_pathfind(graph, 'vancouver', 'new_york')
        # all_routes = [
        #     (['Vancouver', 'New York'], 250.0),
        #     (['Vancouver', 'Beijing', 'New York'], 1600.0)
        # ]
    """
    # Initialize stack with starting node, path, and cost
    stack = [(start, [start], 0)]
    # Store all valid paths found
    all_routes = []
    # Record each step for users to see
    steps = []
    
    while stack:
        current_node, path, cost = stack.pop()
        
        # Record this step for instructional display
        step = {
            'action': f'Pop: {graph.nodes[current_node]["name"]}',
            'stack': [graph.nodes[node]["name"] for node, _, _ in stack],
            'current_path': [graph.nodes[node]["name"] for node in path],
            'cost': cost
        }

        if current_node == goal:
            step['action'] = f'Goal found: {graph.nodes[goal]["name"]}!'
            steps.append(step)
            # Change city IDs to readable names
            for i, city_id in enumerate(path):
                city_name = graph.nodes[city_id]['name']
                path[i] = city_name
            all_routes.append((path, cost))
            continue
        
        neighbors = graph.get_neighbors(current_node)
        neighbor = [(graph.nodes[n]["name"], w) for n, w in neighbors]
        step['neighbors'] = neighbor
            # Add unvisited neighbors to stack
        for neighbor, weight in neighbors:
            # if the city is visited in the current path, skip it to avoid cycles
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor], cost + weight))

        # Record the updated queue state after adding neighbors
        updated_stack = [graph.nodes[node]["name"] for node, _, _ in stack]
        step['updated_stack'] = updated_stack
        steps.append(step)
    
    return (steps, all_routes)
