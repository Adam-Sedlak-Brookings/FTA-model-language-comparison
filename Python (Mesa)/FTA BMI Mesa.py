import matplotlib.pyplot as plt
import mesa
from mesa.space import NetworkGrid
from mesa.time import RandomActivation
import networkx as nx
import numpy as np

class BMIAgent(mesa.Agent):
    """
    An agent with BMI value
    """

    def __init__(self, unique_id, model, alpha, beta):
        super().__init__(unique_id, model)
        
        # Initialize each agents BMI from a ~ 15 + Gamma(alpha, beta)
        self.bmi = 15 + np.random.gamma(alpha, 1/beta)

    def step(self):
        """
        
        """
        # Get all agents connected in the graph to the current agent 
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        # Calculate the mean BMI of all neighboring agents
        mean_bmi = np.mean([agent.bmi for agent in m.grid.iter_cell_list_contents(neighbors)])
        # The difference between agents BMI and mean of neighbors BMI
        dif = mean_bmi - self.bmi
        
        # If the difference is greater than the satificing radius adjust BMI
        if abs(dif) >= self.model.radius:
            # Step size amount to adjust agent BMI by
            step_size = min(abs(dif), 0.1)
            # Move down in BMI if agent heavier than neighbors
            if dif < 0:
                self.bmi -= step_size
            # Move up in BMI if agent lighter than neighbors
            if dif > 0:
                self.bmi += step_size

class FTAModel(mesa.Model):
    """
    A follow the average agent based model of BMI
        N: The number of agent
        rewire_prob: The probability of requiring a node connection when 
                     initializing the Watts-Strogatz graph
        radius: The satisficing radius
        alpha: Gamma shape parameter for initializing agents BMI
        beta: Gamma parameterfor initializing agents BMI
        mean_degree: Number of initial neighbors each agent starts with
    """

    def __init__(self, N=100, rewire_prob=0.1, radius=0.1, alpha=3, beta=0.25, mean_degree=4):
        # Number of agents in the model
        self.num_agents = N
        # Random activation scheduler
        self.schedule = RandomActivation(self)
        # The satisficing radius
        self.radius = radius
        
        # Graph connecting the agents (using Watts-Strogatz algorithm)
        self.G = nx.watts_strogatz_graph(N, mean_degree, rewire_prob)
        self.grid = NetworkGrid(self.G)
        
        # Create agents
        for i, node in enumerate(self.G.nodes()):
            # Create agent i
            a = BMIAgent(i, self, alpha, beta)
            
            # Add agent to schedule and network
            self.schedule.add(a)
            self.grid.place_agent(a, node)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
