#!/usr/bin/env python3
"""
Unit tests for the Graph class
"""
import unittest
from src.graph import Graph


class TestGraph(unittest.TestCase):
    """Test cases for Graph class"""
    
    def setUp(self):
        """Set up a fresh graph for each test"""
        self.graph = Graph()
    
    def test_empty_graph(self):
        """Test that a new graph is empty"""
        self.assertEqual(len(self.graph.nodes), 0)
        self.assertEqual(len(self.graph.edges), 0)

    
    def test_add_single_node(self):
        """Test adding a single node to the graph"""
        self.graph.add_node("vancouver", "Vancouver")
        
        self.assertEqual(len(self.graph.nodes), 1)
        self.assertIn("vancouver", self.graph.nodes)
        self.assertEqual(self.graph.nodes["vancouver"]["name"], "Vancouver")
    
    def test_add_multiple_nodes(self):
        """Test adding multiple nodes to the graph"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_node("calgary", "Calgary")
        
        self.assertEqual(len(self.graph.nodes), 3)
        self.assertIn("vancouver", self.graph.nodes)
        self.assertIn("toronto", self.graph.nodes)
        self.assertIn("calgary", self.graph.nodes)
    
    def test_add_single_edge(self):
        """Test adding a single edge between two nodes"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_edge("vancouver", "toronto", 5.0)
        
        self.assertEqual(len(self.graph.edges["vancouver"]), 1)
        self.assertEqual(self.graph.edges["vancouver"][0], ("toronto", 5.0))
    
    def test_add_multiple_edges_from_same_node(self):
        """Test adding multiple edges from the same node"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_node("calgary", "Calgary")
        
        self.graph.add_edge("vancouver", "toronto", 5.0)
        self.graph.add_edge("vancouver", "calgary", 3.0)
        
        self.assertEqual(len(self.graph.edges["vancouver"]), 2)
    
    def test_add_bidirectional_edges(self):
        """Test adding edges in both directions"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        
        self.graph.add_edge("vancouver", "toronto", 5.0)
        self.graph.add_edge("toronto", "vancouver", 5.0)
        
        self.assertEqual(len(self.graph.edges["vancouver"]), 1)
        self.assertEqual(len(self.graph.edges["toronto"]), 1)
    
    def test_get_neighbors_single(self):
        """Test getting neighbors when node has one neighbor"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_edge("vancouver", "toronto", 5.0)
        
        neighbors = self.graph.get_neighbors("vancouver")
        self.assertEqual(len(neighbors), 1)
        self.assertEqual(neighbors[0], ("toronto", 5.0))
    
    def test_get_neighbors_multiple(self):
        """Test getting neighbors when node has multiple neighbors"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_node("calgary", "Calgary")
        
        self.graph.add_edge("vancouver", "toronto", 5.0)
        self.graph.add_edge("vancouver", "calgary", 3.0)
        
        neighbors = self.graph.get_neighbors("vancouver")
        self.assertEqual(len(neighbors), 2)
    
    def test_get_neighbors_no_edges(self):
        """Test getting neighbors when node has no outgoing edges"""
        self.graph.add_node("vancouver", "Vancouver")
        
        neighbors = self.graph.get_neighbors("vancouver")
        self.assertEqual(len(neighbors), 0)
    
    def test_get_neighbors_nonexistent_node(self):
        """Test getting neighbors of a node that doesn't exist"""
        neighbors = self.graph.get_neighbors("nonexistent")
        self.assertIsNone(neighbors)
    
    def test_get_weight_existing_edge(self):
        """Test getting weight of an existing edge"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_edge("vancouver", "toronto", 5.0)
        
        neighbors = self.graph.get_neighbors("vancouver")
        weight = neighbors[0][1]
        self.assertEqual(weight, 5.0)
    
    def test_get_weight_nonexistent_edge(self):
        """Test getting weight of an edge that doesn't exist"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        
        neighbors = self.graph.get_neighbors("vancouver")
        self.assertEqual(len(neighbors), 0)
    
    def test_different_weights_different_edges(self):
        """Test that different edges have different weights"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_node("calgary", "Calgary")
        
        self.graph.add_edge("vancouver", "toronto", 5.0)
        self.graph.add_edge("vancouver", "calgary", 3.0)
        
        neighbors = self.graph.get_neighbors("vancouver")
        weights = [weight for _, weight in neighbors]
        self.assertNotEqual(weights[0], weights[1])
    
    def test_zero_weight_edge(self):
        """Test adding an edge with zero weight"""
        self.graph.add_node("vancouver", "Vancouver")
        self.graph.add_node("toronto", "Toronto")
        self.graph.add_edge("vancouver", "toronto", 0.0)
        
        neighbors = self.graph.get_neighbors("vancouver")
        self.assertEqual(neighbors[0][1], 0.0)


if __name__ == "__main__":
    unittest.main()