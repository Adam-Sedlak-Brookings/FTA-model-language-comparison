'''
Author: Adam Sedlak
Date: 2022/08/13
'''
import numpy as np


class WattsStrogatzGraph:
    '''
    An a graph object initialized using the Watts-Strogatz algorithm.
    Designed for efficient node connection lookup.

    Attributes
    ----------

    graph : tuple
        A tuple where each index is a tuple of a nodes neighbors.
    n : int
        The number of nodes in this graph.
    rng : numpy Generator (class)
        A random number generator (rng) object that can be seeded.

    Methods
    -------
    rewire(i, j):
        Rewires node i's connection to node j.
    get_neighbors(i):
        Returns a tuple of nodes that node i is connected to.
    '''

    def __init__(self, n, k, beta, rng=np.random.default_rng()):
        '''
        Constructs all a graph using the Watts-Strogatz algorithm and
        all the necessary attributes for a Watts-Strogatz class.

        Parameters
        ----------
            n: int
                The number of nodes in this graph.
            k: int
                The mean degree, the number of adjecent neighbors that the
                graph is initalized with.
            beta: float
                The rewiring probability used to initialize the graph.
            rng : numpy Generator (class), optional
                A random number generator (rng) object to seed graph generation.
                Defaults to a new random seed.
        '''
        def rewire(i, j):
            '''
            Helper function, rewires node i's connection to node j with 
            a new node k, chosen uniformly at random from all node 
            (except for k = i and k already wired to i).

            Parameters
            ----------
            i : int
                Index of the node to be rewired.
            j : int
                Index of the node that i connected to that
                should be rewired.

            Returns
            -------
            None
            '''
            # Do while loop to generate a valid k
            # k can not equal i or be an existing connection
            k = i
            while (k == i or (k in self.graph[i])):
                k = self.rng.integers(0, self.n - 1)

            # Replacing: i -> j with i -> k (in node i)
            self.graph[i].remove(j)
            self.graph[i].add(k)
            # Removing: j -> i (from node j)
            self.graph[j].remove(i)
            # Adding: k -> i (to node k)
            self.graph[k].add(i)

        # Initializing graph varibles
        self.graph = []
        self.n = n
        self.rng = rng

        # Connect every node i to its K nearest neighbors
        # (K/2 left and K/2 right)
        for i in range(n):
            # Creating a set like the following:
            # [-K/2 + i, ..., i - 1, i + 1, ..., i + K/2]
            k_neighbors = set(np.arange(i+int(-k/2), i+1+int(k/2)) % n)
            # Remove self connection
            k_neighbors.remove(i)
            # Add the set to the graph
            self.graph.append(k_neighbors)

        # Give the K/2 right most connections for each node
        # an oppertunity to get rewired
        for i in range(n):
            # Node i's K/2 rightmost neighbors: (i, i + K/2] mod N
            right_neighbors = np.arange(i+1, i+1+int(k/2)) % n
            # Rewire each K/2 right node with probability beta
            for j in right_neighbors:
                # Rewire with probability beta
                if beta > rng.random():
                    rewire(i, j)

        # Cast underlying sets to tuples now that graph is rewired
        for node in range(n):
            self.graph[node] = tuple(self.graph[node])
        # Cast underlying list to tuple for efficiency and network is static
        self.graph = tuple(self.graph)

    def get_neighbors(self, i):
        '''
        Returns a tuple of the nodes connected to node i.

        Parameters
        ----------
        i : int
            Index of the node to be rewired.

        Returns
        -------
        tuple : tuple of node indecies that i is connected to.
        '''
        return self.graph[i]
