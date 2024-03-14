from functools import reduce
import agentpy as ap
import networkx as nx

from model.social_network import SocialNetwork

class Person(ap.Agent):

    model: SocialNetwork
    network: nx.MultiDiGraph
    
    def setup(self, **kwargs):
        self.is_active = self.model.random.random() < 0.005
        self.opinion = self.model.random.betavariate(0.4, 0.4) * 2 - 1
        self.self_belief = self.model.random.random()
        self.social_influence_factor = 0.2
    
    def __get_opinion_influence(self, neighbors):
        
        opinion_similarity = lambda u, v: 1 - (abs(u - v)) / 2.0

        active_opinions = [ n.opinion for n in neighbors if n.is_active and n is not self ]
        neighbor_opinions = [ n.opinion for n in neighbors ]

        active_os = reduce(lambda x, y: x + opinion_similarity(y, self.opinion), active_opinions, 0)
        total_os = reduce(lambda x, y: x + opinion_similarity(y, self.opinion), neighbor_opinions, 0)

        if total_os == 0:
            return 0

        return active_os / total_os

    def __get_relation_influence(self, neighbors):
        
        status_pressure = lambda deg_u, deg_v: deg_u / (deg_u + deg_v)

        degree = nx.degree(self.network, self)

        active_degrees = [self.network.degree(n) for n in neighbors if n.is_active]
        total_degrees = [self.network.degree(n) for n in neighbors]

        active_status = reduce(lambda x, y: x + status_pressure(y, degree), active_degrees, 0)
        total_status = reduce(lambda x, y: x + status_pressure(y, degree), total_degrees, 0)

        if total_status == 0:
            return 0

        return active_status / total_status

    def get_social_influence(self):
        try:
            neighbors = list(self.network.neighbors(self))
            return self.social_influence_factor * self.__get_opinion_influence(neighbors) + (1 - self.social_influence_factor) * self.__get_relation_influence(neighbors)
        
        except nx.exception.NetworkXError:
            print(f'Not found: {self}, {self.model.network.positions[self]}')
    
    def update_opinion(self):
        neighbors = list(self.network.neighbors(self))

        active_opinions = [n.opinion for n in neighbors if n is not self and n.is_active]
        average_opinion = reduce(lambda x, y: x + y, active_opinions) / len(active_opinions)

        self.opinion = self.self_belief * self.opinion + (1 - self.self_belief) * average_opinion
        