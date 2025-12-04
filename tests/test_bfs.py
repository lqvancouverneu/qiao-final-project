#!/usr/bin/env python3
"""
Unit tests for BFS pathfinding
"""
import unittest
from src.graph import Graph
from src.bfs import bfs_pathfind


class TestBFS(unittest.TestCase):
    """Test cases for BFS pathfinding"""
    
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

    
    def test_bfs_simple_path(self):
        """Test BFS finding a simple direct path A -> B"""
        steps, path, cost = bfs_pathfind(self.graph, start="A", goal="B")
        
        # Path should be A -> B (direct connection)
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], "City A")
        self.assertEqual(path[1], "City B")
        self.assertEqual(cost, 5.0)
        # Should have recorded steps
        self.assertGreater(len(steps), 0)
    
    def test_bfs_longer_path(self):
        """Test BFS finding a longer path A -> B -> C"""
        steps, path, cost = bfs_pathfind(self.graph, start="A", goal="C")
        
        # Path should be A -> B -> C
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], "City A")
        self.assertEqual(path[1], "City B")
        self.assertEqual(path[2], "City C")
        self.assertEqual(cost, 15.0)  # 5.0 + 10.0
    
    def test_bfs_no_path(self):
        """Test BFS when no path exists"""
        # Add isolated nodes
        self.graph.add_node("X", "City X")
        self.graph.add_node("Y", "City Y")
        
        steps, path, cost = bfs_pathfind(self.graph, start="A", goal="Y")
        
        # Should return empty path and infinite cost
        self.assertEqual(len(path), 0)
        self.assertEqual(cost, float('inf'))
    
    def test_bfs_same_start_and_goal(self):
        """Test BFS when start and goal are the same"""
        steps, path, cost = bfs_pathfind(self.graph, start="A", goal="A")
        
        # Path should contain only the starting node
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], "City A")
        self.assertEqual(cost, 0)
    
    def test_bfs_fewest_hops(self):
        """Test that BFS finds path with fewest hops"""
        # Multiple paths to E:
        # Path 1: A -> B -> C -> E (3 hops)
        # Path 2: A -> D -> E (2 hops)
        # BFS should find Path 2 (fewest hops)
        
        steps, path, cost = bfs_pathfind(self.graph, start="A", goal="E")
        
        # Should find A -> D -> E (2 edges = fewest hops)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], "City A")
        self.assertEqual(path[1], "City D")
        self.assertEqual(path[2], "City E")


if __name__ == "__main__":
    unittest.main()