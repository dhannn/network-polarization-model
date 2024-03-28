import unittest
from functools import reduce
import agentpy as ap
import networkx as nx

# Import the Person class
from src.model.combined import Person
from src.model.combined import SocialNetwork


class TestPerson(unittest.TestCase):

    def setUp(self) -> None:
        self.model = SocialNetwork({'population': 5}, mode="M", mode2="+")
        self.agents = ap.AgentList(self.model, 5, Person)

        initial_states = [
            {"is_active": False, "opinion": 0.8, "self_belief": 0.5, "social_influence_factor": 0.3},
            {"is_active": True, "opinion": -0.6, "self_belief": 0.7, "social_influence_factor": 0.2},
            {"is_active": False, "opinion": 0.4, "self_belief": 0.9, "social_influence_factor": 0.1},
            {"is_active": True, "opinion": -0.4, "self_belief": 0.6, "social_influence_factor": 0.4},
            {"is_active": False, "opinion": -0.7, "self_belief": 0.3, "social_influence_factor": 0.5},
        ]

        for i, agent in enumerate(self.agents):
            agent.is_active = initial_states[i]["is_active"]
            agent.opinion = initial_states[i]["opinion"]
            agent.self_belief = initial_states[i]["self_belief"]
            agent.social_influence_factor = initial_states[i]["social_influence_factor"]
            # agent.print_agent_traits()

    def test_get_opinion_influence(self):
        neighbors = ap.AgentList(self.model, 2, Person)
        initial_states = [
            {"is_active": True, "opinion": -0.6, "self_belief": 0.7, "social_influence_factor": 0.2},
            {"is_active": False, "opinion": 0.4, "self_belief": 0.9, "social_influence_factor": 0.1}
        ]
        for i, agent in enumerate(neighbors):
            agent.is_active = initial_states[i]["is_active"]
            agent.opinion = initial_states[i]["opinion"]
            agent.self_belief = initial_states[i]["self_belief"]
            agent.social_influence_factor = initial_states[i]["social_influence_factor"]
        influence = self.agents[0].get_opinion_influence(neighbors)

        # Got 3/11 from manual calc
        self.assertAlmostEqual(influence, 3 / 11, delta=0.001)  # Using delta to account for floating point error


    def test_get_relation_influence(self):
        neighbors = ap.AgentList(self.model, 2, Person)
        initial_states = [
            {"is_active": True, "opinion": -0.6, "self_belief": 0.7, "social_influence_factor": 0.2},
            {"is_active": False, "opinion": 0.4, "self_belief": 0.9, "social_influence_factor": 0.1}
        ]
        for i, agent in enumerate(neighbors):
            agent.is_active = initial_states[i]["is_active"]
            agent.opinion = initial_states[i]["opinion"]
            agent.self_belief = initial_states[i]["self_belief"]
            agent.social_influence_factor = initial_states[i]["social_influence_factor"]

        # Create a network with agents[0] and its neighbors
        network = nx.Graph()
        network.add_node(self.agents[0])  # Add agent[0] to the network

        # Add edges to represent relationships with neighbors
        for neighbor in neighbors:
            network.add_edge(self.agents[0], neighbor)

        # Assign the network to self.agents[0].network
        self.agents[0].network = network
        influence = self.agents[0].get_relation_influence(neighbors)

        # (1/3)/(1/3+1/3) = 0.5

        self.assertAlmostEqual(influence, 1/2, delta=0.001)

    def test_get_social_influence(self):
        neighbors = ap.AgentList(self.model, 2, Person)
        initial_states = [
            {"is_active": True, "opinion": -0.6, "self_belief": 0.7, "social_influence_factor": 0.2},
            {"is_active": False, "opinion": 0.4, "self_belief": 0.9, "social_influence_factor": 0.1},

        ]
        for i, agent in enumerate(neighbors):
            agent.is_active = initial_states[i]["is_active"]
            agent.opinion = initial_states[i]["opinion"]
            agent.self_belief = initial_states[i]["self_belief"]
            agent.social_influence_factor = initial_states[i]["social_influence_factor"]

        # Create a network with agents[0] and its neighbors
        network = nx.Graph()
        network.add_node(self.agents[0])  # Add agent[0] to the network

        # Add edges to represent relationships with neighbors
        for neighbor in neighbors:
            network.add_edge(self.agents[0], neighbor)

        # Assign the network to self.agents[0].network
        self.agents[0].network = network
        influence = self.agents[0].get_social_influence()

        #print(influence)
        self.assertAlmostEqual(influence, 0.3 * 3/11 + (1-0.3)*0.5, delta=0.001)

    def test_update_opinion(self):
        neighbors = ap.AgentList(self.model, 3, Person)
        initial_states = [
            {"is_active": True, "opinion": -0.6, "self_belief": 0.7, "social_influence_factor": 0.2},
            {"is_active": False, "opinion": 0.4, "self_belief": 0.9, "social_influence_factor": 0.1},
            {"is_active": True, "opinion": -0.4, "self_belief": 0.6, "social_influence_factor": 0.4}
        ]
        for i, agent in enumerate(neighbors):
            agent.is_active = initial_states[i]["is_active"]
            agent.opinion = initial_states[i]["opinion"]
            agent.self_belief = initial_states[i]["self_belief"]
            agent.social_influence_factor = initial_states[i]["social_influence_factor"]

        # Create a network with agents[0] and its neighbors
        network = nx.Graph()
        network.add_node(self.agents[0])  # Add agent[0] to the network

        # Add edges to represent relationships with neighbors
        for neighbor in neighbors:
            network.add_edge(self.agents[0], neighbor)

        # Assign the network to self.agents[0].network
        self.agents[0].network = network
        #print(self.agents[0].opinion)
        self.agents[0].update_opinion()
        #print(self.agents[0].opinion)
        self.assertAlmostEqual(self.agents[0].opinion, 0.5*0.8 + ((1-0.5)*((-0.6+-0.4)/2)), delta=0.001)



if __name__ == '__main__':
    unittest.main()
