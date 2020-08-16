import pacman

"""
    INSTRUCTION: 
    python pacman.py -h for the usage
    
    The code below is written to run each level in the assignment.

    Switching map using either
        -r <n=N,m=M,level=L>: generate N*M map at level L( 1 <= i <= 4)
    or
        -l <name of layout>: use the provided layout in folder layouts/

    When both of these commands is called, generate map will be prioritized
"""

"""
LV1: Pac-man know the food’s position in map and monsters do not appear in map.
There is only one food in the map.
"""
# Using BFS
# pacman.main(
#    'python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=bfs -f 0.2')

# Using DFS
# pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=dfs')

# using UCS
# pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=ucs')
#pacman.main('python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs')

# Using A*
# Manhattan heuristic
# pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=astar,heuristic=mHeur')
# Euclidean heuristic
# pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=astar,heuristic=eHeur')
# Using GBFS:
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=gbfs')

"""
Level 2: monsters stand in the place ever (never move around). If Pac-man pass
through the monster or vice versa, game is over. There is still one food in the map
and Pac-man know its position
"""
# Using UCS
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=2 -p SafeSearchAgent -g LazyGhost')

# Using A* - manhattan heuristic
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=2 -p SafeSearchAgent -g LazyGhost -a fn=astar,heuristic=mHeur')
# - euclidean heuristic
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=2 -p SafeSearchAgent -g LazyGhost -a fn=astar,heuristic=eHeur')

"""
Level 3: Pac-man cannot see the foods if they are outside Pacman’s nearest threestep. It means that Pac-man just only scan all the adjacent him (8 tiles x 3). There
are many foods in the map. Monsters just move one step in any valid direction (if
any) around the initial location at the start of the game. Each step Pacman go,
each step Monsters move
"""

# EXPECTIMAX
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p ExpectimaxAgent -g StupidGhost')

# MINIMAX
# pacman.main(
#    'python pacman.py -r n=20,m=20,level=4 -p MinimaxAgent -g StupidGhost')

# AB pruning
# pacman.main(
#    'python pacman.py -r n=20,m=20,level=4 -p AlphaBetaAgent -g StupidGhost')

# --- LOCAL SEARCH + EXPECTIMAX
# pacman.main(
#    'python pacman.py -r n=20,m=20,level=4 -p ExplorerAgent -g StupidGhost')

# --- LOCAL SEARCH + AB pruning
# pacman.main(
#    'python pacman.py -r n=20,m=20,level=4 -p ExplorerAgentII -g StupidGhost -a depth=4')

"""
Level 4 (difficult): map is closed. Monsters will seek and kill Pac-man. Pac-man
want to get food as much as possible. Pacman will die if at least one monster
passes him. It is ok for monsters go through each other. Each step Pacman go,
each step Monsters move. The food is so many.
"""
# Using Expectimax
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p ExpectimaxAgent -g DirectionalGhost -a evalFn=custom')

# Using Minimax
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p MinimaxAgent -g DirectionalGhost -a evalFn=custom')

# Using AB pruning
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p MinimaxAgent -g DirectionalGhost -a evalFn=custom')


# LOCAL SEARCH + EXPECTIMAX
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p ExplorerAgent -g DirectionalGhost')

# LOCAL SEARCH + EXPECTIMAX
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p ExplorerAgentII -g DirectionalGhost -a depth=4')
