#!/usr/bin/env python3
"""
Unit tests for DFS pathfinding
"""
import unittest
from src.graph import Graph
from src.dfs import dfs_pathfind


class TestDFS(unittest.TestCase):
    """Test cases for DFS pathfinding"""
    
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

    
    def test_dfs_simple_path(self):
        """Test DFS finding a simple direct path A -> B"""
        steps, all_routes = dfs_pathfind(self.graph, start="A", goal="B")
        
        # Should find at least one path
        self.assertGreater(len(all_routes), 0)
        
        # Check if A -> B path exists
        paths = [path for path, _ in all_routes]
        self.assertIn(["City A", "City B"], paths)
        
        # Check cost for A -> B
        for path, cost in all_routes:
            if path == ["City A", "City B"]:
                self.assertEqual(cost, 5.0)
    
    def test_dfs_longer_path(self):
        """Test DFS finding a longer path A -> B -> C"""
        steps, all_routes = dfs_pathfind(self.graph, start="A", goal="C")
        
        # Should find at least one path to C
        self.assertGreater(len(all_routes), 0)
        
        # Check if A -> B -> C path exists
        paths = [path for path, _ in all_routes]
        self.assertIn(["City A", "City B", "City C"], paths)
        
        # Check cost for A -> B -> C
        for path, cost in all_routes:
            if path == ["City A", "City B", "City C"]:
                self.assertEqual(cost, 15.0)  # 5.0 + 10.0
    
    def test_dfs_no_path(self):
        """Test DFS when no path exists"""
        # Add isolated nodes
        self.graph.add_node("X", "City X")
        self.graph.add_node("Y", "City Y")
        
        steps, all_routes = dfs_pathfind(self.graph, start="A", goal="Y")
        
        # Should return empty routes list (no path exists)
        self.assertEqual(len(all_routes), 0)
    
    def test_dfs_same_start_and_goal(self):
        """Test DFS when start and goal are the same"""
        steps, all_routes = dfs_pathfind(self.graph, start="A", goal="A")
        
        # Should find one path: just A
        self.assertEqual(len(all_routes), 1)
        
        path, cost = all_routes[0]
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], "City A")
        self.assertEqual(cost, 0)
    
    def test_dfs_finds_all_routes(self):
        """Test that DFS finds ALL possible routes to goal"""
        steps, all_routes = dfs_pathfind(self.graph, start="A", goal="E")
        
        # Should find multiple routes to E:
        # Route 1: A -> B -> C -> E (cost: 5 + 10 + 2 = 17)
        # Route 2: A -> D -> E (cost: 3 + 4 = 7)
        
        self.assertGreaterEqual(len(all_routes), 2)
        
        # Extract costs
        costs = [cost for _, cost in all_routes]
        self.assertIn(17.0, costs)  # A -> B -> C -> E
        self.assertIn(7.0, costs)   # A -> D -> E


if __name__ == "__main__":
    unittest.main()