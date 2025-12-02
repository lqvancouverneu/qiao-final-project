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
            route_dijkstra, cost_dijkstra = dijkstra_pathfind(graph, start=start, goal=goal)
            route_dijkstra_joined = " -> ".join(route_dijkstra)
            print("Lowest cost(using Dijkstra):")
            print(route_dijkstra_joined, "Cost:", cost_dijkstra)

        case '2':
            route_bfs, cost_bfs = bfs_pathfind(graph, start=start, goal=goal)
            route_bfs_joined = " -> ".join(route_bfs)
            print("Fewest stops(using BFS):")
            print(route_bfs_joined, "Cost:", cost_bfs)

        case '3':
            all_routes = dfs_pathfind(graph, start=start, goal=goal)
            def get_sort_key(x):
                return x[1]
            all_routes.sort(key=get_sort_key)
            print("All DFS Paths (sorted by cost):")
            for route_dfs, cost_dfs in all_routes:
                route_dfs_joined = " -> ".join(route_dfs)
                print(route_dfs_joined, "Cost:", cost_dfs)

        case '4':
            start, goal = get_user_input()

        case _:
            print("Invalid choice. Please select 1, 2, 3 or 4.")
