# Follow the Average Agent-Based Model Comparison

## Overview
This repository compares various different agent-based modeling (ABM) libraries, languages, and designs by implementing the follow the average (FTA) model—developed by Hammond and Ornstein (2014)**[1]**. This is a good resource for those curious about ABM performance across software, learning new programming languages (e.g., Mesa expert curious about the Agents.jl), and/or those interested in the FTA model.
The FTA model was implemented in NetLogo, Python, and Julia comparing performance, accuracy, and ease of implementation. An analysis was performed as well comparing the accuracy of implementations in Julia, Mesa, and NetLogo. Three Python models were created and analyzed: Mesa, the Python library for creating ABMs; Custom, an ABM written in base python; and Numpy, an ABM written using matrices.

## Software
* Python: Some of the python was written in Jupyter Notebooks.
* Julia: Model was developed in a Pluto Notebook (this is the Julia version of Jupyter) and uses some of the Pluto UI tools for visualization/interaction
* NetLogo: Code was written using Netlogo version 6.0.2



## Analysis
| Language          | Base Model Time  (mean ± sd) | Runs to Average | Scaling With # Agents $y=ax^2+bx+c$   | Lines of Code   | GUI?                                 |
|-------------------|------------------------------|-----------------|-------------------------------------|-------|--------------------------------------|
| Julia (Agents.jl) | 32ms ± 8.2ms                 | 150             | $O(n)$, b=7E-4                        | 15-20 | Yes, but limited support (as of now) |
| Python (Numpy)    | 9.86 ms ± 601 µs             | 700             | $O(n^2)$*, a=3E-7                     | 9     | No                                   |       |
| Python (Custom)   | 411ms ± 50ms                 | 30              | $O(n)$, b=4.5E-3                      | 100+  | No                                   |       |
| Python (Mesa)     | 732ms ± 50ms                 | 30              | $O(n)$, b=7.8E-3                      | 30-40 | Yes, limited docs/ examples          |       |
| NetLogo           | 104ms ± 50ms**               | 1000             | $O(n^2)$***, a=2E-5                    | 30-40 | Yes, very easy basically free        |       |

\* Python (Numpy) can be made to scale linearly with large $n$ by using sparse arrays

\** This is for only using one core

\*** NetLogo could no longer load models after $n > 5000$

## Model Notes
* Agents.jl
  * Library had a bit of a learning curve but was easy once you knew what you needed
  * Julia is still pretty new so there are fewer resources and messier docs (e.g., found a typo on the Graphs.jl page
   * The [graphs docs](https://docs.juliahub.com/Graphs/VJ6vx/1.4.0/generators/#Graphs.SimpleGraphs.watts_strogatz-Tuple{Integer,%20Integer,%20Real}) say the following which is incorrect (with respect to both the definition and implementation in Julia): "For β = 1, the graph will remain a 1-lattice, and for β = 0, all edges will be rewired randomly"
  * Unicode character support and Pluto made condense and assessable 

* Numpy
  * Note that this code **technically** doesn't run a FTA model because all agents update their BMIs at the same time. However, the notebook includes a test comparing how this update rule effects the model outcome (interestingly it does not effect the model outcome, although there may be an edge case I have missed).
  * Slower FTA version written in Numpy was written could be speed up with Python JIT.
  * Simultaneous update version of the model was fastest of all models implemented.
  * Applying numba jit to fastest numpy model got speed down to 2.20ms ± 152 µs!
  
* Custom
  * There is a lot of code needed for this implementation and a better version can be found in the Numpy implementation.
  * Improves over the Mesa implementation, my guess is that most models done without libraries are about x2 faster

* Mesa
  * Fastest to implement (although personal experience in Python helped a lot)
  * The Mesa docs were decent and there were lots of external Python resources
  * Slowest of all the models implemented

* NetLogo
  * NetLogo syntax is a bit confusing (e.g., no equals signs).
  * GUI implementation was easy to use and required little additional work
  * I couldn't figure out how to benchmark NetLogo so these are some rough estimates. My guess is that with multicores and headless state NetLogo performance is quite good

## Citations

**[1]** Hammond, R. A., &amp; Ornstein, J. T. (2014). A model of social influence on body mass index. Annals of
the New York Academy of Sciences, 1331(1), 34-42.

**[2]** Watts, D. J.; Strogatz, S. H. (1998). "Collective dynamics of 'small-world' networks" (PDF). Nature. 393 (6684): 440–442.

## Contact
For questions contact: asedlak@brookings.edu
