'''
Author: Adam Sedlak 
Date: 2022/08/13
'''

import numpy as np
from WattsStrogatzGraph import WattsStrogatzGraph

class ABMSocialInfluenceBMI:
    '''
    An agent-based model of social influence on obesity status.

    Attributes
    ----------
    rng : numpy Generator (class)
        A random number generator (rng) object that can be seeded
    agents : int
        Number of model agents
    bmi : float np.array()
        An array of all agents BMI's
    network : WattsStrogatzGraph (class)
        The Watts-Strogatz network between agents
    radius : float
        The satisficing radius used for this model
    ticks : int
        Number of time ticks this model will run for

    Methods
    -------
    run():
        Runs the specified model.
    '''

    def __init__(self, satisficing_radius, rewiring_prob,
                 bmi_distr=lambda agents, rng: 15+rng.gamma(3, 4, agents),
                 agents=100, mean_degree=4, ticks=200, seed=None):
        '''
        Constructs all the necessary attributes for an agent-based model of
        social influence on obesity status. Defaults to parameters outlined
        in model overview.

        Parameters
        ----------
            satisficing_radius: float
                Satisficing radius threshold parameter used to determine
                if agent will change BMI.
            rewiring_prob: float
                The rewiring probability used to initialize agent network
                via Watts-Strogatz alogrithm (also called beata).
            bmi_distr: function, optional
                Function used to initialize an array of agent BMI's. Takes
                two parameters the number of agents and a numpy RNG Generator.
                Defaults to a 15 + Gamma(3, 4) distribution.
            agents: int, optional
                The number of agents used in the model. Defaults to 100.
            mean_degree: int, optional
                Then mean degree parameter used to initialize agent network
                via Watts-Strogatz algorithm (also called K).
            ticks: int, optional
                Number of time ticks to run the model for. Defaults to 200.
            seed: int, optional
                A model seed that can be used to reproduce a simulation.
                Defaults to a new random seed.
        '''
        self.rng = np.random.default_rng(seed)
        self.agents = agents
        self.bmi = bmi_distr(agents, self.rng)
        self.network = WattsStrogatzGraph(agents, mean_degree,
                                          rewiring_prob, self.rng)
        self.radius = satisficing_radius
        self.ticks = ticks

    def run(self):
        '''
        Runs the specified model.

        Parameters
        ----------
        None

        Returns
        -------
        Tuple of model results in the following order;
        
        Initial BMIs: np.array(), float
            An array of the populations initial BMIs, before the 
            model has run.
        Final BMIs: np.array(), float
            An array of the populations final BMIs, after the 
            model has run.
        Mean BMIs over time: np.array(), float
            A time series of the mean population BMI over 
            the course of the model.
        '''
        # Save the initial BMI's of the population
        initial_bmi = np.copy(self.bmi)
        # Create an array to save running mean through model ticks
        mean_bmi = np.empty(self.ticks)
        # Array of agent indices 0 to N-1
        indices = np.arange(self.agents)

        # Running model for specified number of ticks
        for t in range(self.ticks):
            # Start each tick by shuffling the agent indices
            self.rng.shuffle(indices)

            # Loop over agents in random order giving each an opportunity
            # to update its BMI.
            for agent in indices:
                # Get the indices of all neighbors linked to the current node
                neighbors = self.network.get_neighbors(agent)
                # Using the current node's neighbors, compute the mean BMI
                mean_bmi_neighbors = np.mean(np.take(self.bmi, neighbors))
                # Determine the difference between agents BMI and mean
                bmi_dif = self.bmi[agent] - mean_bmi_neighbors
                # Update BMI if difference is greater than satisficing radius
                if abs(bmi_dif) > self.radius:
                    # Step size is at most 0.1 or bmi_dif (whichever is smaller)
                    delta = min(abs(bmi_dif), 0.1)
                    # If agent BMI is above mean, move DOWN towards mean
                    if bmi_dif > 0:
                        self.bmi[agent] -= delta
                    # Otherwise, agent is below mean BMI and should move UP
                    else:
                        self.bmi[agent] += delta

            # Save the mean population BMI for current tick
            mean_bmi[t] = np.mean(self.bmi)

        # Return initial BMIs, final BMIs, and time series of mean BMIs
        return initial_bmi, self.bmi, mean_bmi
