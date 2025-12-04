#!/usr/bin/env python3
"""
Unit tests for Dijkstra's shortest path algorithm
"""
import unittest
from src.graph import Graph
from src.dijkstra import dijkstra_pathfind


class TestDijkstra(unittest.TestCase):
    """Test cases for Dijkstra's algorithm"""
    
    def setUp(self):
        """Set up a test graph for each test"""
        self.graph = Graph()
        
        # Create a simple graph:
        #   A --5--> B --10--> C
        #   |                  |
        #   3                  2
        #   |                  |
        #   v                  v
        #   D --4-----------> E
        
        for node_id in ["A", "B", "C", "D", "E"]:
            self.graph.add_node(node_id, f"City {node_id}")
        
        self.graph.add_edge("A", "B", 5.0)
        self.graph.add_edge("B", "C", 10.0)
        self.graph.add_edge("A", "D", 3.0)
        self.graph.add_edge("D", "E", 4.0)
        self.graph.add_edge("C", "E", 2.0)

    
    def test_dijkstra_simple_path(self):
        """Test Dijkstra finding a simple direct path A -> B"""
        steps, path, cost = dijkstra_pathfind(self.graph, start="A", goal="B")
        
        # Path should be A -> B (direct connection)
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], "City A")
        self.assertEqual(path[1], "City B")
        self.assertEqual(cost, 5.0)
        # Should have recorded steps
        self.assertGreater(len(steps), 0)
    
    def test_dijkstra_shortest_cost_path(self):
        """Test Dijkstra finding the lowest cost path"""
        steps, path, cost = dijkstra_pathfind(self.graph, start="A", goal="E")
        
        # Two possible paths to E:
        # Path 1: A -> B -> C -> E (cost: 5 + 10 + 2 = 17)
        # Path 2: A -> D -> E (cost: 3 + 4 = 7)
        # Dijkstra should find Path 2 (lowest cost)
        
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], "City A")
        self.assertEqual(path[1], "City D")
        self.assertEqual(path[2], "City E")
        self.assertEqual(cost, 7.0)
    
    def test_dijkstra_no_path(self):
        """Test Dijkstra when no path exists"""
        # Add isolated nodes
        self.graph.add_node("X", "City X")
        self.graph.add_node("Y", "City Y")
        
        steps, path, cost = dijkstra_pathfind(self.graph, start="A", goal="Y")
        
        # Should return empty path and infinite cost
        self.assertEqual(len(path), 0)
        self.assertEqual(cost, float('inf'))
    
    def test_dijkstra_same_start_and_goal(self):
        """Test Dijkstra when start and goal are the same"""
        steps, path, cost = dijkstra_pathfind(self.graph, start="A", goal="A")
        
        # Path should contain only the starting node
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], "City A")
        self.assertEqual(cost, 0)
    
    def test_dijkstra_vs_fewest_hops(self):
        """Test that Dijkstra prioritizes lowest cost, not fewest hops"""
        graph = Graph()
        
        # Create nodes
        for node_id in ["A", "B", "C", "D", "F"]:
            graph.add_node(node_id, f"City {node_id}")
        
        # Expensive direct path
        graph.add_edge("A", "B", 100.0)
        graph.add_edge("B", "F", 100.0)
        
        # Cheap but longer path
        graph.add_edge("A", "C", 1.0)
        graph.add_edge("C", "D", 1.0)
        graph.add_edge("D", "F", 1.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="F")
        
        # Dijkstra should find cheapest: A -> C -> D -> F (cost: 3)
        # Not fewest hops: A -> B -> F (cost: 200)
        self.assertEqual(cost, 3.0)
        self.assertEqual(len(path), 4)
    
    def test_dijkstra_multiple_paths_same_cost(self):
        """Test Dijkstra with multiple paths having the same cost"""
        graph = Graph()
        
        for node_id in ["A", "B", "C", "D"]:
            graph.add_node(node_id, f"City {node_id}")
        
        # Two equal cost paths
        graph.add_edge("A", "B", 5.0)
        graph.add_edge("B", "D", 5.0)
        
        graph.add_edge("A", "C", 5.0)
        graph.add_edge("C", "D", 5.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="D")
        
        # Should find one valid path with cost 10
        self.assertEqual(cost, 10.0)
        self.assertEqual(len(path), 3)
    
    def test_dijkstra_complex_graph(self):
        """Test Dijkstra on a more complex graph"""
        graph = Graph()
        
        nodes = ["A", "B", "C", "D", "E", "F"]
        for node_id in nodes:
            graph.add_node(node_id, f"City {node_id}")
        
        # Complex connections
        graph.add_edge("A", "B", 4.0)
        graph.add_edge("A", "C", 2.0)
        graph.add_edge("B", "C", 1.0)
        graph.add_edge("B", "D", 5.0)
        graph.add_edge("C", "D", 8.0)
        graph.add_edge("C", "E", 10.0)
        graph.add_edge("D", "E", 2.0)
        graph.add_edge("D", "F", 6.0)
        graph.add_edge("E", "F", 3.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="F")
        
        # Should find optimal path
        self.assertGreater(len(steps), 0)
        self.assertGreater(len(path), 0)
        self.assertNotEqual(cost, float('inf'))
    
    def test_dijkstra_single_node_graph(self):
        """Test Dijkstra on a single node graph"""
        graph = Graph()
        graph.add_node("A", "City A")
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="A")
        
        self.assertEqual(len(path), 1)
        self.assertEqual(cost, 0)
    
    def test_dijkstra_zero_weight_edges(self):
        """Test Dijkstra with zero weight edges"""
        graph = Graph()
        
        for node_id in ["A", "B", "C"]:
            graph.add_node(node_id, f"City {node_id}")
        
        graph.add_edge("A", "B", 0.0)
        graph.add_edge("B", "C", 0.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="C")
        
        self.assertEqual(cost, 0.0)
        self.assertEqual(len(path), 3)
    
    def test_dijkstra_finds_optimal_avoiding_expensive_edge(self):
        """Test that Dijkstra avoids expensive edges when possible"""
        graph = Graph()
        
        for node_id in ["A", "B", "C", "D"]:
            graph.add_node(node_id, f"City {node_id}")
        
        # Expensive direct edge
        graph.add_edge("A", "D", 1000.0)
        
        # Cheaper multi-hop path
        graph.add_edge("A", "B", 1.0)
        graph.add_edge("B", "C", 1.0)
        graph.add_edge("C", "D", 1.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="D")
        
        # Should avoid expensive edge
        self.assertEqual(cost, 3.0)
        self.assertNotIn("D", path[1:])  # D is not second node
    
    def test_dijkstra_all_paths_from_source(self):
        """Test that Dijkstra explores all possible paths"""
        graph = Graph()
        
        for node_id in ["A", "B", "C", "D", "E"]:
            graph.add_node(node_id, f"City {node_id}")
        
        graph.add_edge("A", "B", 1.0)
        graph.add_edge("A", "C", 4.0)
        graph.add_edge("B", "C", 2.0)
        graph.add_edge("B", "D", 5.0)
        graph.add_edge("C", "D", 1.0)
        graph.add_edge("D", "E", 3.0)
        
        steps, path, cost = dijkstra_pathfind(graph, start="A", goal="E")
        
        # Should record multiple steps exploring different nodes
        self.assertGreater(len(steps), 1)


class TestDijkstraVsOtherAlgorithms(unittest.TestCase):
    """Test to demonstrate Dijkstra vs other algorithms"""
    
    def setUp(self):
        """Set up comparison graph"""
        self.graph = Graph()
        
        for node_id in ["A", "B", "C", "D", "E", "F"]:
            self.graph.add_node(node_id, f"City {node_id}")
        
        # Multiple paths with different characteristics
        self.graph.add_edge("A", "B", 100.0)
        self.graph.add_edge("B", "F", 100.0)
        
        self.graph.add_edge("A", "C", 1.0)
        self.graph.add_edge("C", "D", 1.0)
        self.graph.add_edge("D", "E", 1.0)
        self.graph.add_edge("E", "F", 1.0)
    
    def test_dijkstra_guarantees_lowest_cost(self):
        """Test that Dijkstra guarantees the lowest cost path"""
        steps, path, cost = dijkstra_pathfind(self.graph, start="A", goal="F")
        
        # Dijkstra should find: A -> C -> D -> E -> F (cost: 4)
        # Not: A -> B -> F (cost: 200, fewer hops)
        self.assertEqual(cost, 4.0)
        self.assertLess(cost, 200.0)


if __name__ == "__main__":
    unittest.main()