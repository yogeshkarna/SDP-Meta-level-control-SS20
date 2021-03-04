# SDP-Meta-level-control-SS20

# Members 
1. Alex Jude
2. Madhumetha Ramesh
3. Yogeshkarna Govindaraj

Reference: 
  Svegliato, J., Wray, K. H., & Zilberstein, S. (2018). Meta-level control of anytime algorithms with online performance prediction. In IJCAI International Joint Conference on Artificial Intelligence (Vols. 2018-July). https://doi.org/10.24963/ijcai.2018/208 
  
# About the project
Anytime algorithms are those algorithms which provide a trade-off between time of computation and the quality of the solution. In real-time real-world use-cases, the decision of when the anytime algorithm has to be interrupted so as to yield the "best" solution (with respect to time and quality) is decided by meta-level control. 

Previous work on meta-level control were primarily focused on significant amount of offline work, which made it infeasible for real-time problems. The task of preprocessing before initializing the anytime algorithm, requires  execution and evaluation of all the plausible instances of the use-case. This is computationaly expensive, time consuming and infeasible and incompatible with any changes to the problem in hand.

Workspace 
- /data contains anytime algorithm quality acqired in '.json' format
- /plots contains plots of meta-level control algorithm 
- mlc.py contains the python program for meta-level control 
