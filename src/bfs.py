from collections import deque
from typing import List, Tuple
from src.graph import Graph


def bfs_pathfind(graph: Graph, start: str, goal: str) -> Tuple[List[dict], List[str], float]:
    """
    Performs Breadth-First Search to find the shortest path (fewest hops) from start to goal.
    
    Uses a queue (FIFO) to explore nodes level by level, ensuring the first path found
    has the minimum number of edges. Records each step for users to see.
    
    Args:
        graph (Graph): The flight graph containing cities (nodes) and routes (edges)
        start (str): Starting city ID (e.g., 'vancouver')
        goal (str): Destination city ID (e.g., 'new_york')
    
    Returns:
        Tuple[List[Dict], List[str], float]:
            - steps: List of dictionaries containing step-by-step actions for users to see
              Each step includes: action, queue state, visited nodes, current path, cost, neighbors
            - path: List of city names from start to goal (empty list if no path exists)
            - cost: Total cost of the path (sum of edge weights). Returns float('inf') if no path exists
    
    Time Complexity: O(V + E) where V is vertices and E is edges
    Space Complexity: O(V) for the queue and visited set
    
    Characteristics:
        - Finds path with FEWEST HOPS (minimum number of edges)
        - Does not guarantee lowest cost (use Dijkstra for that)
        - Explores all neighbors at current depth before moving deeper
        - Marks visited nodes to avoid revisiting
    
    Example:
        steps, path, cost = bfs_pathfind(graph, 'vancouver', 'new_york')
        # path = ['Vancouver', 'Toronto', 'New York']
        # cost = 350.0
        # steps = [step1, step2, step3, ...]
    """
     # Initialize queue with starting node (FIFO - First In First Out)
    queue = deque([(start, [start], 0.0)])
    # Track all visited nodes to avoid revisiting them
    previous_level = {start}
    # Store each step for users to see
    steps = []

    while queue:
        # Dequeue node from front of queue (FIFO behavior)
        current_node, path, cost = queue.popleft()
        
        # Record this step for instructional display
        step = {
            'action': f'Dequeue: {graph.nodes[current_node]["name"]}',
            'queue': [graph.nodes[node]["name"] for node, _, _ in queue],
            'previous_level': [graph.nodes[node]["name"] for node in previous_level],
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
            return (steps, path, cost)
        
        # Get all neighbors (outgoing flights from current city)
        neighbors = graph.get_neighbors(current_node)
        neighbor_names = [graph.nodes[neighbor]["name"] for neighbor, _ in neighbors]
        step['neighbors'] = neighbor_names
  

        # Explore all unvisited neighbors by adding them to queue
        # Iterate over neighbors and each iteration we will get neighbor and weight
        for neighbor, weight in neighbors:
            # if the city is visited in the current path, skip it to avoid cycles
            if neighbor not in previous_level:
                queue.append((neighbor, path + [neighbor], cost + weight))
                # Mark as visited immediately to ensure each node is processed once
                previous_level.add(neighbor)
        
        updated_queue = [graph.nodes[node]["name"] for node, _, _ in queue]
        step['updated_queue'] = updated_queue
        steps.append(step)

    # No path found - return empty path and infinite cost
    return (steps, [], float('inf'))
