import unittest
from functools import reduce
import agentpy as ap
import networkx as nx

# Import the Person class
from src.model.person import Person

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.model = ap.Model()
        # Create the network with specified edges
        self.G = nx.MultiDiGraph()

        # Add nodes with correct identifiers
        self.G.add_node(0, is_active=False, opinion=0.8, self_belief=0.5, social_influence_factor=0.3)
        self.G.add_node(1, is_active=True, opinion=-0.6, self_belief=0.7, social_influence_factor=0.2)
        self.G.add_node(2, is_active=False, opinion=0.4, self_belief=0.9, social_influence_factor=0.1)
        self.G.add_node(3, is_active=True, opinion=-0.4, self_belief=0.6, social_influence_factor=0.4)
        self.G.add_node(4, is_active=False, opinion=-0.7, self_belief=0.3, social_influence_factor=0.5)

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]  # Corrected edges
        self.G.add_edges_from(edges)

        # Print out the edges of the network
        print("Edges of the network:")
        print(list(self.G.edges()))

    def test_get_opinion_influence(self):
        # Test when all neighbors have active opinions
        self.G.nodes

        person = Person(model=self.model, network=self.G)
        influence = person._Person__get_opinion_influence(self.G.neighbors(0))
        self.assertAlmostEqual(influence, 0.5)  # Update expected value based on calculation

    def test_get_relation_influence(self):
        # Test when all neighbors have same degrees
        person = Person(model=self.model, network=self.G)
        influence = person._Person__get_relation_influence(self.G.neighbors(0))
        self.assertAlmostEqual(influence, 0.5)  # Update expected value based on calculation

    def test_get_social_influence(self):
        # Test when all neighbors have active opinions and same degrees
        person = Person(model=self.model, network=self.G)
        influence = person.get_social_influence()
        expected_influence = 0.2 * 0.5 + 0.8 * 0.5  # Update expected value based on calculation
        self.assertAlmostEqual(influence, expected_influence)

    def test_update_opinion(self):
        # Test update opinion function
        person = Person(model=self.model, network=self.G)
        person.update_opinion()
        # Add assertions to test the updated opinion

if __name__ == '__main__':
    unittest.main()

