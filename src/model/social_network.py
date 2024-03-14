import agentpy as ap
import networkx as nx

from model.person import Person

class SocialNetwork(ap.Model):


    def __init__(self, params, mode="M", mode2="M"):
        super().__init__(params)
        self.social_temperature_mode = mode
        self.polarity_mode = mode2

    def setup(self):
        self.population = self.p['population']
        
        self.agents = ap.AgentDList(self, self.population, Person)

        self.pos_agents = [ a for a in self.agents if a.opinion >= 0 ]
        self.neg_agents = [ a for a in self.agents if a.opinion < 0 ]
        
        subgraph1: nx.Graph = nx.powerlaw_cluster_graph(len(self.pos_agents), 3, 0.5)
        subgraph2: nx.Graph = nx.powerlaw_cluster_graph(len(self.neg_agents), 3, 0.5)
        

        mapping1 = { i: list(self.pos_agents)[i] for i in range(len(self.pos_agents)) }
        mapping2 = { i: list(self.neg_agents)[i] for i in range(len(self.neg_agents)) }

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

            if self.polarity_mode == "+": # positive only
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
            elif self.polarity_mode == "-": # negative only
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
            else: # default is mixed
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

        self.active_agents = [ agent for agent in self.agents if agent.is_active ]
        self.activated_agents = [ agent for agent in self.agents if agent.is_active ]

        self.agents.network = network
        self.network = network
    
    def update(self):
        with open('test', 'a') as file:
            file.write(f'{self.model.t}\t Opinion: {self.agents[0].opinion}\t is_aticve: {self.agents[0].is_active}\t si: {self.agents[0].get_social_influence()}\n')

    
    def step(self):

        if abs(max(self.agents.opinion) - min(self.agents.opinion)) < 0.1 or self.t >= 100:
            self.stop()

        self.activated_agents = self.active_agents.copy()

        self.activated_agents: ap.AgentList
        active_agent: Person

        for active_agent in self.activated_agents:
            neighbors = [ n for n in self.network.neighbors(active_agent) ]
            
            neighbor: Person
            for neighbor in neighbors:
                if neighbor not in self.activated_agents:
                    neighbor.is_active = True
                    self.active_agents.append(neighbor)
                
                social_influence = neighbor.get_social_influence()

                if neighbor.is_active and social_influence >= neighbor.self_belief:
                    neighbor.update_opinion()
