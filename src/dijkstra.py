import heapq
from typing import List, Tuple
from src.graph import Graph


def dijkstra_pathfind(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Performs Dijkstra's shortest path algorithm to find the minimum cost path from start to goal.
    
    Uses a min-heap (priority queue) to always explore the node with lowest accumulated cost first.
    Guarantees finding the optimal (lowest cost) path. Records each step for users to see.
    
    Args:
        graph (Graph): The flight graph containing cities (nodes) and routes (edges with weights)
        start (str): Starting city ID (e.g., 'vancouver')
        goal (str): Destination city ID (e.g., 'new_york')
    
    Returns:
        Tuple[List[Dict], List[str], float]:
            - steps: List of dictionaries containing step-by-step actions for users to see
              Each step includes: action, queue state, current path, cost, neighbors, updated queue
            - path: List of city names from start to goal (empty list if no path exists)
            - cost: Total cost of the shortest path (sum of edge weights). Returns float('inf') if no path exists
    
    Time Complexity: O((V + E) log V) where V is vertices and E is edges
    Space Complexity: O(V) for the priority queue and cost dictionary
    
    Algorithm Overview:
        1. Start with the source node at cost 0
        2. Use a min-heap to always process the lowest-cost unvisited node next
        3. For each node, relax all outgoing edges (update neighbor costs if lower cost found)
        4. Stop when goal node is reached with minimum cost
        5. Continue exploring to ensure optimality
    
    Characteristics:
        - Finds path with LOWEST COST (minimum total edge weight)
        - Does not guarantee fewest hops (use BFS for that)
        - Works with non-negative edge weights
        - Greedy algorithm that always picks lowest cost node next
        - Guarantees optimal solution for single-source shortest path
    
    Differences from other algorithms:
        - vs BFS: Dijkstra minimizes cost, BFS minimizes hops
        - vs DFS: Dijkstra finds one optimal path, DFS finds all paths
    
    Example:
        steps, path, cost = dijkstra_pathfind(graph, 'vancouver', 'new_york')
        # path = ['Vancouver', 'Calgary', 'Toronto', 'New York']
        # cost = 550.0  (lowest cost path)
        # steps = [step1, step2, step3, ...]
    
    Raises:
        Does not raise exceptions; returns empty path and infinite cost if no solution exists
    """
    # Initialize min-heap with starting node at cost 0
    queue = [(0, start, [start])]
    # Track the minimum cost to reach each node (for cheaper)
    cost = {start: 0}
    # Store each step for users to see
    steps = []
    
    # Continue until all reachable nodes are explored
    while queue:
        # Pop node with lowest cost from min-heap (greedy choice)
        current_cost, current_node, path = heapq.heappop(queue)
        
        # Record this step for instructional display
        step = {
            'action': f'Pop: {graph.nodes[current_node]["name"]} (Cost: {current_cost})',
            'queue': [(current_cost, graph.nodes[node]["name"]) for current_cost, node, _ in queue],
            'current_path': [graph.nodes[node]["name"] for node in path],
            'cost': current_cost
        }

        # Check if we reached the goal - Dijkstra guarantees this is the minimum cost path
        if current_node == goal:
            step['action'] = f'Goal found: {graph.nodes[goal]["name"]}!'
            steps.append(step)
            # Change city IDs to readable names
            for i, city_id in enumerate(path):
                city_name = graph.nodes[city_id]['name']
                path[i] = city_name
            return (steps, path, current_cost)
        
        # Get all outgoing flights from current city
        neighbors = graph.get_neighbors(current_node)
        neighbor_names = [graph.nodes[n]["name"] for n, _ in neighbors]
        step['neighbors'] = neighbor_names

        # Update neighbor costs if cheaper path found
        for neighbor, weight in graph.get_neighbors(current_node):
            # Calculate new cost to reach neighbor through current node
            new_cost = current_cost + weight
            # If neighbor hasn't been visited or found cheaper path, update it
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))

        # Record the updated heap state after adding neighbors
        updated_queue = [(current_cost, graph.nodes[node]["name"]) for current_cost, node, _ in queue]
        step['updated_queue'] = updated_queue
        steps.append(step)

    # No path found - return empty path and infinite cost
    return (steps, [], float('inf'))
