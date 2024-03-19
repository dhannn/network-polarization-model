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
            #agent.print_agent_traits()


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
        self.agents[0].__get_opinion_influence(neighbors)
        print("----------")
        #print(influence)
        print("try")
        for agent in self.agents:
            print(f"Agent ID: {agent.id}")
            print(f"\tis_active: {agent.is_active}")
            print(f"\topinion: {agent.opinion}")
            print(f"\tself_belief: {agent.self_belief}")
            print(f"\tsocial_influence_factor: {agent.social_influence_factor}")


    #def test_get_opinion_influence(self):
        # Test __get_opinion_influence function
     #   print("agasg")
        #for i, agent in enumerate(self.agents):
            #agent.print_agent_traits()

        #person = self.persons[0]
        #opinion_influence = person._Person__get_opinion_influence(list(self.network.neighbors(person)))
        #self.assertAlmostEqual(opinion_influence, 1.000, places=3)  # Placeholder value for testing


if __name__ == '__main__':
    unittest.main()