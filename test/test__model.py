import unittest

import agentpy as ap

from src.model.social_network import SocialNetwork
from src.model.person import Person

class TestSocialNetwork(unittest.TestCase):
    
    # Test Cases
    # H+ H- H mixed
    # M+ M- M mixed
    # L
    # HL
    # HM
    # ML
    # HML

    # H >= 0.8 abs
    # 0.8 > M > 0.2 abs
    # L <= 0.2 abs
    

    agents = []
    
    def setUp(self) -> None:

    # initialize agents
    # need at least 6 agents H+, H-, M+, M-, L+, L-
        model = ap.Model()

        # Add 6 Person objects to the list
        self.agents = []
        for _ in range(6):
            person = Person(model=model)  # Pass the model to each Person instance
            self.agents.append(person)

        
        opinion_values = [0.9, -0.9, 0.5, -0.5, 0.1, -0.1]
        for agent, opinion in zip(self.agents, opinion_values):
            agent.opinion = opinion
            agent.is_active = False
        
        for idx, agent in enumerate(self.agents):
            print(f"Agent {idx + 1}:")
            print(f"  Is Active: {agent.is_active}")
            print(f"  Opinion: {agent.opinion}")
            print(f"  Self Belief: {agent.self_belief}")
            print(f"  Social Influence Factor: {agent.social_influence_factor}")
            print()

    def test__activate_inital_nodes__high_temp_positive_polarity(self):
        SocialNetwork.activateInitialNodes(self.agents, polarity_mode="+", social_temperature_mode="H")
        
        expected = [ True, False, False, False, False, False ]
        actual = [ agent.is_active for agent in self.agents ]
        self.assertListEqual(expected, actual, f'Expected {expected}, returns, {actual}')
    
    def test__activate_inital_nodes__mid_temp_negative_polarity(self):
        SocialNetwork.activateInitialNodes(self.agents, polarity_mode="-", social_temperature_mode="M")
        
        expected = [False, False, False, True, False, False]
        actual = [ agent.is_active for agent in self.agents ]
        self.assertListEqual(expected, actual, f'Expected {expected}, returns, {actual}')
        
        
    def test_activate_initial_nodes_low_temp_mixed_polarity(self):
        SocialNetwork.activateInitialNodes(self.agents, polarity_mode="M", social_temperature_mode="L")
        
        expected = [False, False, False, False, True, True]
        actual = [ agent.is_active for agent in self.agents ]
        self.assertListEqual(expected, actual, f'Expected {expected}, returns, {actual}')

    def test_activate_initial_nodes_high_low_temp_positive_polarity(self):
        SocialNetwork.activateInitialNodes(self.agents, polarity_mode="+", social_temperature_mode="HL")
        
        expected = [True, False, False, False, True, False]
        actual = [ agent.is_active for agent in self.agents ]
        self.assertListEqual(expected, actual, f'Expected {expected}, returns, {actual}')
    
    def test_activate_initial_nodes_high_low_temp_negative_polarity(self):
        SocialNetwork.activateInitialNodes(self.agents, polarity_mode="-", social_temperature_mode="HL")
        
        expected = [False, True, False, False, False, True]
        actual = [ agent.is_active for agent in self.agents ]
        self.assertListEqual(expected, actual, f'Expected {expected}, returns, {actual}')
    
    def test_activate_initial_nodes_high_low_temp_mixed_polarity(self):
        pass
        
    