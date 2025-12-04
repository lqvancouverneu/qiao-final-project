from typing import List, Tuple


class Graph:
    """
    A directed weighted graph representation for flight networks.
    
    Stores cities as nodes and flight routes as edges with costs (distances or prices).
    Supports adding nodes and edges, and querying neighbor connections.
    
    Attributes:
        nodes (Dict): Dictionary mapping node IDs to node data
                      Format: {node_id: {'name': city_name}, ...}
        edges (Dict): Dictionary mapping node IDs to their outgoing edges
                      Format: {node_id: [(neighbor_id, weight), ...], ...}
    
    Example:
        graph = Graph()
        graph.add_node('yvr', 'Vancouver')
        graph.add_node('yyz', 'Toronto')
        graph.add_edge('yvr', 'yyz', 350.0)
        
        neighbors = graph.get_neighbors('yvr')
        # neighbors = [('yyz', 350.0)]
    """
    def __init__(self):
        """
        Initialize an empty graph with no nodes or edges.
        
        Initializes two empty dictionaries:
        - nodes: stores city information
        - edges: stores flight routes and their costs
        """
        # Dictionary to store all cities (nodes) with their names
        self.nodes = {
            # node_id1: {'name': city name1},
            # node_id2: {'name': city name2},
            # ...
        }
        # Dictionary to store all flight routes (edges) with their costs
        self.edges = {
            # node_id1: [(to_node1, weight1), (to_node2, weight2), ...],
            # node_id2: [(to_node3, weight3), (to_node4, weight4), ...],
            # ...
        }
    
    def add_node(self, node_id: str, name: str):
        """
        Add a city (node) to the graph.
        
        Args:
            node_id (str): Unique identifier for the city (e.g., 'yvr', 'vancouver')
            name (str): Human-readable name of the city (e.g., 'Vancouver')
        
        Example:
            graph.add_node('yvr', 'Vancouver')
            graph.add_node('yyz', 'Toronto')
        """
        # Store the city name in nodes dictionary
        self.nodes[node_id] = {'name': name}
        # Initialize an empty list for edges from this node
        self.edges[node_id] = []
    
    def add_edge(self, from_node: str, to_node: str, weight: float):
        """
        Add a flight route (edge) from one city to another with a cost.
        
        Creates a directed edge, so from_node -> to_node is one-way.
        To create bidirectional flights, call add_edge twice.
        
        Args:
            from_node (str): Starting city ID (e.g., 'yvr')
            to_node (str): Destination city ID (e.g., 'yyz')
            weight (float): Cost of the flight (distance, price, time, etc.)
        
        Example:
            # Direct flight from Vancouver to Toronto
            graph.add_edge('yvr', 'yyz', 350.0)
            
            # Bidirectional flight
            graph.add_edge('yvr', 'yyz', 350.0)
            graph.add_edge('yyz', 'yvr', 350.0)
        """
        # Add the destination city and cost as a tuple to the starting city's edge list
        # This creates a directed edge: from_node -> to_node with weight
        self.edges[from_node].append((to_node, weight))
    
    def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        """
        Get all outgoing flights from a city.
        
        Args:
            node_id (str): The city ID to query (e.g., 'yvr')
        
        Returns:
            List[Tuple[str, float]]: List of (neighbor_id, cost) tuples
            Returns None if node doesn't exist
        
        Example:
            neighbors = graph.get_neighbors('yvr')
            # neighbors = [('yyz', 350.0), ('sea', 150.0)]
            
            # Check if node exists
            neighbors = graph.get_neighbors('nonexistent')
            # neighbors = None
        """
        # Get the list of outgoing edges (flights) from the given node
        # Returns None if the node doesn't exist in the graph
        neighbors = self.edges.get(node_id)
        return neighbors
