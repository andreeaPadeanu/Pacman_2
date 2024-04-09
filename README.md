# Pacman_2
 multiagent

In this project, we have constructed agents to solve the Pacman problem, including ghosts. The code has been modified in the multiAgents.py file.

Question 1: Building a reflex agent.
The task is to improve the functioning of the ReflexAgent. Inside it, GameState can be queried to obtain information about the game state. A reflex agent that plays the game effectively must consider the locations for food and ghosts. A well-implemented agent should be able to clean up the entire testClassic layout.

Question 2: Minimax.
We have implemented the MinimaxAgent in multiAgents.py. We observed that if Pacman estimates that it will die (inevitably), then it will prefer to end the game as quickly as possible (thus not consuming moves). This is not rational behavior in such a situation (with random ghosts), but in the case of minimax, this behavior is correct.

Question 3: Alpha-beta pruning.
For this question, the AlphaBetaAgent needs to be implemented.

Question 4: Expectimax.
In minimax or alpha-beta pruning, it is assumed that you are playing against ghosts that take optimal actions – which is often not the case. For this question, we have implemented the ExpectimaxAgent, which models a probabilistic behavior of the ghosts.
