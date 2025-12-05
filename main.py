import re
from src.graph import Graph
from src.bfs import bfs_pathfind
from src.dfs import dfs_pathfind
from src.dijkstra import dijkstra_pathfind


graph = Graph()

cities = [
    ("vancouver", "Vancouver"),
    ("new_york", "New York"),
    ("london", "London"),
    ("beijing", "Beijing"),
    ("daqing", "Daqing"),
    ("seoul", "Seoul"),
]

for city_id, name in cities:
    graph.add_node(node_id=city_id, name=name)

edges = [
    ("vancouver", "new_york", 250.0),
    ("vancouver", "london", 1200.0),
    ("vancouver", "beijing", 1400.0),
    ("vancouver", "seoul", 1000.0),
    ("new_york", "beijing", 1200.0),
    ("new_york", "seoul", 1100.0),
    ("new_york", "london", 400.0),
    ("london", "beijing", 800.0),
    ("london", "seoul", 600.0),
    ("beijing", "seoul", 100.0),
    ("beijing", "daqing", 200.0),
]

for from_node, to_node, weight in edges:
    graph.add_edge(from_node=from_node, to_node=to_node, weight=weight)
    graph.add_edge(from_node=to_node, to_node=from_node, weight=weight) 

# User interaction
def get_user_input():
    print("Available cities:")
    for _, name in cities:
        print(f"- {name}")

    user_input_is_not_valid = True
    while user_input_is_not_valid:
        start = input("Enter the starting city: ").strip().lower()
        start = re.sub(r'\s+', '_', start)  # Replace multiple spaces with single underscore
        goal = input("Enter the destination city: ").strip().lower()
        goal = re.sub(r'\s+', '_', goal)  # Replace multiple spaces with single underscore

        if start not in graph.nodes or goal not in graph.nodes:
            print("One or both of the specified cities do not exist in the graph.")
        else:
            user_input_is_not_valid = False

    return start, goal

start, goal = get_user_input()

while True:
    choice = input("Choose flight finding method (1.Cheapest, 2.Fewest Stops, 3.All Flights, 4.Reenter cities): ").strip()
    match choice:
        case '1':
            steps, route_dijkstra, cost_dijkstra = dijkstra_pathfind(graph, start=start, goal=goal)

            # Ask user preference
            step_by_step = input("View step-by-step? (y/n): ").strip().lower() == 'y'
            
            print(f"\n[Dijkstra] Start: {start} → {goal}\n")
            #Enumerate will return a list of tuples. 
            #And each item in the tuples is the index and a single step.
            #Loop through the list, for each iteration we will get the index and the step.
            for i, step in enumerate(steps, 1):
                print(f"Step {i}/{len(steps)}:")
                #find the value of action in the step dictionary
                print(f"  Action: {step['action']}")
                print(f"  Queue: {step['queue']}")
                print(f"  Path so far: {' → '.join(step['current_path'])}", f"(Cost: {step['cost']})")
                # Check if 'neighbors' key exists in the step dictionary to find it is the last step or not
                if 'neighbors' in step:
                    print(f"  Neighbors: {step['neighbors']}")
                    print(f"  Updated Queue: {step['updated_queue']}")
                print()
            
                # Pause only if step-by-step mode and not last step
                if step_by_step and i < len(steps):
                    user_input = input("Press Enter for next step, or 'a' to show all remaining: ").strip().lower()
                    if user_input == 'a':
                        step_by_step = False

            if route_dijkstra:
                print(f"✓ Lowest cost path: {' → '.join(route_dijkstra)} (Cost: {cost_dijkstra})")
            else:
                print("✗ No path found")

        case '2':
            steps, route_bfs, cost_bfs = bfs_pathfind(graph, start=start, goal=goal)

            # Ask user preference
            step_by_step = input("View step-by-step? (y/n): ").strip().lower() == 'y'

            print(f"\n[BFS] Start: {start} → {goal}\n")
            for i, step in enumerate(steps, 1): # [(index1, step1), (index2, step2) ...]
                print(f"Step {i}/{len(steps)}:")
                print(f"  Action: {step['action']}")
                print(f"  Queue: {step['queue']}")
                print(f"  Previous level: {step['previous_level']}")
                print(f"  Path so far: {' → '.join(step['current_path'])}", f"(Cost: {step['cost']})")
                if 'neighbors' in step:
                    print(f"  Neighbors: {step['neighbors']}")
                    print(f"  Updated Queue: {step['updated_queue']}")
                print()
            
                # Pause only if step-by-step mode and not last step
                if step_by_step and i < len(steps):
                    user_input = input("Press Enter for next step, or 'a' to show all remaining steps: ").strip().lower()
                    if user_input == 'a':
                        step_by_step = False  # Show all remaining steps without pausing

            if route_bfs:
                print(f"✓ Path found: {' → '.join(route_bfs)} (Cost: {cost_bfs})")
            else:
                print("✗ No path found")

        case '3':
            steps, all_routes = dfs_pathfind(graph, start=start, goal=goal)
            # Sort all routes by cost for better readability
            def get_sort_key(x):
                return x[1]
            all_routes.sort(key=get_sort_key)
            # \n is new line
            print(f"\n[DFS] Start: {start} → {goal}\n")
            
            # Ask user preference
            step_by_step = input("View step-by-step? (y/n): ").strip().lower() == 'y'
    
            for i, step in enumerate(steps, 1):
                print(f"Step {i}/{len(steps)}:")
                print(f"  Action: {step['action']}")
                print(f"  Stack: {step['stack']}")
                print(f"  Path so far: {' → '.join(step['current_path'])}", f"(Cost: {step['cost']})")
                if 'neighbors' in step:
                    print(f"  Neighbors: {step['neighbors']}")
                    print(f"  Updated Stack: {step['updated_stack']}")
                print()
            
                # Pause only if step-by-step mode and not last step
                if step_by_step and i < len(steps):
                    user_input = input("Press Enter for next step, or 'a' to show all remaining steps: ").strip().lower()
                    if user_input == 'a':
                        step_by_step = False  # Show all remaining steps without pausing
            
            print("All DFS Paths (sorted by cost):")
            for route_dfs, cost_dfs in all_routes:
                print(f"  {' → '.join(route_dfs)} (Cost: {cost_dfs})")

        case '4':
            start, goal = get_user_input()

        case _:
            print("Invalid choice. Please select 1, 2, 3 or 4.")
