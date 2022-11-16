# Agent-based Model of Social Influence on Obesity Status

## Overview
This project implements an agent based model, based on the work by Hammond and Ornstein **[1]**, that explores the effects of social influence on obesity status (BMI). Agents are connected in a network constructed using the Watts-Strogatz algorithm **[2]**. Every time tick agents consider the mean BMI of their neighbors and move their BMI towards the mean BMI of their neighbors if the mean difference is greater than a “satisficing radius”.

### Files
`WattsStrogatzGraph.py`: Class that implements a graph (or network) of nodes initialized using the Watts–Strogatz algorithm.

`ABMSocialInfluenceBMI.py`: Class that implements the agent based model described above. Utlizes `WattsStrogatzGraph` for agent network.

`Model Visualization and Writeup.ipynb`: Jupyter notebook containing visualizations and a writeup of model results (includes a markdown of this README as well).

### Dependencies
`WattsStrogatzGraph.py` and `ABMSocialInfluenceBMI.py` written using numpy version 1.21.5.

### Examples
**Running a AMB**

    from ABMSocialInfluenceBMI import ABMSocialInfluenceBMI
    import numpy as np

    # Creating a new ABM with a satisficing radius of 0.4
    # and a rewiring probability 0.1
    model = ABMSocialInfluenceBMI(0.4, 0.1)
    # Running model
    final_bmi, intital_bmi, mean_bmi = model.run()
**Creating a graph/network**

    >>> from WattsStrogatzGraph import WattsStrogatzGraph
    # Creating a new network with 150 nodes, 4 neighbors, and
    # a rewiring probability 0.15
    >>> network = WattsStrogatzGraph(150, 4, 0.15)
    # Getting 3rd nodes neighbors (zero indexed)
    >>> network.get_neighbors(2)
    
    
## API Documentation

### `ABMSocialInfluenceBMI`
An agent-based model of social influence on obesity status. Takes a "satisficing radius" (`radius`) and rewiring probability (`rewiring_prob`), all other parameters are optional. BMI defaults to a
$X \sim 15+\text{Gamma}(\alpha = 3, \beta = 0.25)$ distribution, agents defaults to $100$, mean degree defaults to $4$, and ticks defaults to $200$. Model can also be seeded with an optional `seed` argument to create reproducible results.

### `WattsStrogatzGraph`
A graph constructed using the Watts–Strogatz algorithm, used as an underlying network for `ABMSocialInfluenceBMI`. Takes the number of nodes in the network (`n`), the mean degree (`k`), and rewiring probability (`beta`).
