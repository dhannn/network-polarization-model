from functools import reduce
import agentpy as ap
import networkx as nx



class SocialNetwork(ap.Model):
    def __init__(self, params, mode="M", mode2="M"):
        super().__init__(params)
        self.social_temperature_mode = mode
        self.polarity_mode = mode2

    def setup(self):
        self.population = self.p['population']

        self.agents = ap.AgentDList(self, self.population, Person)

        self.pos_agents = [a for a in self.agents if a.opinion >= 0]
        self.neg_agents = [a for a in self.agents if a.opinion < 0]

        subgraph1: nx.Graph = nx.powerlaw_cluster_graph(len(self.pos_agents), 3, 0.5)
        subgraph2: nx.Graph = nx.powerlaw_cluster_graph(len(self.neg_agents), 3, 0.5)

        mapping1 = {i: list(self.pos_agents)[i] for i in range(len(self.pos_agents))}
        mapping2 = {i: list(self.neg_agents)[i] for i in range(len(self.neg_agents))}

        nx.relabel_nodes(subgraph1, mapping1, copy=False)
        nx.relabel_nodes(subgraph2, mapping2, copy=False)

        network = nx.Graph()

        network.add_nodes_from(subgraph1.nodes())
        network.add_nodes_from(subgraph2.nodes())
        network.add_edges_from(subgraph1.edges())
        network.add_edges_from(subgraph2.edges())

        for agent in self.agents:
            agent: Person
            abs_opinion = abs(agent.opinion)

            if self.polarity_mode == "+":  # positive only
                if self.social_temperature_mode == "H":
                    agent.is_active = agent.opinion >= 0.8
                elif self.social_temperature_mode == "L":
                    agent.is_active = 0 <= agent.opinion <= 0.2
                elif self.social_temperature_mode == "HM":
                    agent.is_active = agent.opinion >= 0.8 or 0.2 < agent.opinion < 0.8
                elif self.social_temperature_mode == "HL":
                    agent.is_active = agent.opinion >= 0.8 or 0 <= agent.opinion <= 0.2
                elif self.social_temperature_mode == "ML":
                    agent.is_active = 0.2 < agent.opinion < 0.8 or 0 <= agent.opinion <= 0.2
                elif self.social_temperature_mode == "HML":
                    agent.is_active = True
                else:  # Default to 'M' (medium) if an invalid mode is provided
                    agent.is_active = 0.2 < agent.opinion < 0.8
            elif self.polarity_mode == "-":  # negative only
                if self.social_temperature_mode == "H":
                    agent.is_active = agent.opinion <= -0.8
                elif self.social_temperature_mode == "L":
                    agent.is_active = 0 >= agent.opinion >= -0.2
                elif self.social_temperature_mode == "HM":
                    agent.is_active = agent.opinion <= -0.8 or -0.2 > agent.opinion > -0.8
                elif self.social_temperature_mode == "HL":
                    agent.is_active = agent.opinion <= -0.8 or 0 >= agent.opinion >= -0.2
                elif self.social_temperature_mode == "ML":
                    agent.is_active = -0.2 > agent.opinion > -0.8 or 0 >= agent.opinion >= -0.2
                elif self.social_temperature_mode == "HML":
                    agent.is_active = True
                else:  # Default to 'M' (medium) if an invalid mode is provided
                    agent.is_active = -0.2 > agent.opinion > -0.8
            else:  # default is mixed
                if self.social_temperature_mode == "H":
                    agent.is_active = abs_opinion >= 0.8
                elif self.social_temperature_mode == "L":
                    agent.is_active = abs_opinion <= 0.2
                elif self.social_temperature_mode == "HM":
                    agent.is_active = abs_opinion >= 0.8 or 0.2 < abs_opinion < 0.8
                elif self.social_temperature_mode == "HL":
                    agent.is_active = abs_opinion >= 0.8 or abs_opinion <= 0.2
                elif self.social_temperature_mode == "ML":
                    agent.is_active = 0.2 < abs_opinion < 0.8 or abs_opinion <= 0.2
                elif self.social_temperature_mode == "HML":
                    agent.is_active = True
                else:  # Default to 'M' (medium) if an invalid mode is provided
                    agent.is_active = 0.2 < abs_opinion < 0.8

        u: Person
        for u in subgraph1.nodes():
            v: Person
            for v in subgraph2.nodes():
                u_prime = self.random.choice([u, v])
                v_prime = u if u_prime == v else v
                if abs(u.opinion - v.opinion) <= 0.2 and self.random.random() < 0.1:
                    network.add_edge(u_prime, v_prime)

        nx.write_gml(network, 'test.gml', lambda x: str(x))

        self.active_agents = [agent for agent in self.agents if agent.is_active]
        self.activated_agents = [agent for agent in self.agents if agent.is_active]

        self.agents.network = network
        self.network = network

    def update(self):
        with open('test', 'a') as file:
            file.write(
                f'{self.model.t}\t Opinion: {self.agents[0].opinion}\t is_aticve: {self.agents[0].is_active}\t si: {self.agents[0].get_social_influence()}\n')

    def step(self):

        if abs(max(self.agents.opinion) - min(self.agents.opinion)) < 0.1 or self.t >= 100:
            self.stop()

        self.activated_agents = self.active_agents.copy()

        self.activated_agents: ap.AgentList
        active_agent: Person

        for active_agent in self.activated_agents:
            neighbors = [n for n in self.network.neighbors(active_agent)]

            neighbor: Person
            for neighbor in neighbors:
                if neighbor not in self.activated_agents:
                    neighbor.is_active = True
                    self.active_agents.append(neighbor)

                social_influence = neighbor.get_social_influence()

                if neighbor.is_active and social_influence >= neighbor.self_belief:
                    neighbor.update_opinion()

class Person(ap.Agent):
    model: SocialNetwork
    network: nx.MultiDiGraph

    def setup(self, **kwargs):
        self.is_active = self.model.random.random() < 0.005
        self.opinion = self.model.random.betavariate(0.4, 0.4) * 2 - 1
        self.self_belief = self.model.random.random()
        self.social_influence_factor = 0.2

    def get_opinion_influence(self, neighbors):

        opinion_similarity = lambda u, v: 1 - (abs(u - v)) / 2.0

        active_opinions = [n.opinion for n in neighbors if n.is_active and n is not self]
        neighbor_opinions = [n.opinion for n in neighbors]

        active_os = reduce(lambda x, y: x + opinion_similarity(y, self.opinion), active_opinions, 0)
        total_os = reduce(lambda x, y: x + opinion_similarity(y, self.opinion), neighbor_opinions, 0)

        if total_os == 0:
            return 0

        return active_os / total_os

    def get_relation_influence(self, neighbors):

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
            return self.social_influence_factor * self.get_opinion_influence(neighbors) + (
                        1 - self.social_influence_factor) * self.get_relation_influence(neighbors)

        except nx.exception.NetworkXError:
            print(f'Not found: {self}, {self.model.network.positions[self]}')

    def update_opinion(self):
        neighbors = list(self.network.neighbors(self))

        active_opinions = [n.opinion for n in neighbors if n is not self and n.is_active]
        average_opinion = reduce(lambda x, y: x + y, active_opinions) / len(active_opinions)

        self.opinion = self.self_belief * self.opinion + (1 - self.self_belief) * average_opinion

    def print_agent_traits(self):
        """Prints the traits (attributes) of all agents."""
        print(f"\tis_active: {self.is_active}")
        print(f"\topinion: {self.opinion}")
        print(f"\tself_belief: {self.self_belief}")
        print(f"\tsocial_influence_factor: {self.social_influence_factor}")
        print("-" * 30)  # Print a separator for clarity

