import pacman

"""
    INSTRUCTION about map using either 
    -r <n=N,m=M,level=L>: generate N*M map at level L( 1 <= i <= 4)
    or 
    -l <name of layout>: use the existing layout in folder layouts/

    When both of these commands is called, generate map will be prioritized
"""

"""
LV1: Pac-man know the food’s position in map and monsters do not appear in map. 
There is only one food in the map.
"""
# Using BFS
#pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=bfs')

# Using DFS
#pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=dfs')

# using UCS
#pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=ucs')

# Using A*
# Manhattan heuristic
#pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=astar,heuristic=mHeur')
# Euclidean heuristic
#pacman.main('python pacman.py -r n=20,m=20,level=1 -p SearchAgent -a fn=astar,heuristic=eHeur')


"""
Level 2: monsters stand in the place ever (never move around). If Pac-man pass
through the monster or vice versa, game is over. There is still one food in the map
and Pac-man know its position
"""
# Using UCS
#pacman.main('python pacman.py -r n=20,m=20,level=2 -p SafeSearchAgent -g LazyGhost')

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


"""
Level 4 (difficult): map is closed. Monsters will seek and kill Pac-man. Pac-man
want to get food as much as possible. Pacman will die if at least one monster
passes him. It is ok for monsters go through each other. Each step Pacman go,
each step Monsters move. The food is so many.
"""
# Using Expectimax
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p ExpectimaxAgent -g DirectionalGhost -f 0')

#pacman.main('python pacman.py -p ExpectimaxAgent -g DirectionalGhost -f 0')

# Using Minimax
# pacman.main(
#     'python pacman.py -r n=20,m=20,level=4 -p MinimaxAgent -g DirectionalGhost -f 0')

#pacman.main('python pacman.py -p MinimaxAgent -g DirectionalGhost -f 0')

# _---------------------------EXPLORER
pacman.main(
    'python pacman.py -l mediumClassic -p ExplorerAgent -g DirectionalGhost')
