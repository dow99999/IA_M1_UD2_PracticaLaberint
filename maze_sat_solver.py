"""
1    o x x x x x x o
2            x
3      x x   x   x
4        x   x   x
5    x   x
6    x   x x x x x x
7                   
8    x x x x   x x x
9    u         x     
  
     A B C D E F G H


top-left start

direction:
 left->right
 top->bottom

u: starting point
o: target
x: wall
 : path
"""

from pysat.solvers import Solver
from pysat.formula import CNF

from MazeSat import MazeSat as M

maze_matrix = [
  [ M.FLAG, M.WALL, M.WALL, M.WALL, M.WALL, M.WALL, M.WALL, M.FLAG ],
  [ M.PATH, M.PATH, M.PATH, M.PATH, M.WALL, M.PATH, M.PATH, M.PATH ],
  [ M.PATH, M.WALL, M.WALL, M.PATH, M.WALL, M.PATH, M.WALL, M.PATH ],
  [ M.PATH, M.PATH, M.WALL, M.PATH, M.WALL, M.PATH, M.WALL, M.PATH ],
  [ M.WALL, M.PATH, M.WALL, M.PATH, M.PATH, M.PATH, M.PATH, M.PATH ],
  [ M.WALL, M.PATH, M.WALL, M.WALL, M.WALL, M.WALL, M.WALL, M.WALL ],
  [ M.PATH, M.PATH, M.PATH, M.PATH, M.PATH, M.PATH, M.PATH, M.PATH ],
  [ M.WALL, M.WALL, M.WALL, M.WALL, M.PATH, M.WALL, M.WALL, M.WALL ],
  [ M.USER, M.PATH, M.PATH, M.PATH, M.PATH, M.WALL, M.PATH, M.PATH ]
]

maze = M()
maze.load_maze_from_matrix(maze_matrix)

solver = Solver(name="g4")  # usamos Glucose4
cnf = CNF()


# Preparamos las clausulas:

# Donde esta el usuario es por donde empezamos el camino
# Importante: En caso que el usuario tenga mas de una opcion para empezar el camino hay que forzar una direccion manualmente (con assumptions, por ejemplo)
cnf.append(maze.get_user_clause())

# Un muro del laberinto no es un camino valido
cnf.extend(maze.get_all_wall_clauses())

# Se quiere llegar al menos a un objetivo
cnf.append(maze.get_all_flags_clause())

# Desde una posicion cualquiera se puede generar una o dos posiciones libres dependiendo de si se esta en el inicio del camino o en medio
cnf.extend(maze.get_all_maze_route_clauses())

# print(cnf.clauses)
# print(len(cnf.clauses))

solver.append_formula(cnf)

# Resolvemos el laberinto:
solver.solve()
# print(solver.get_core())

# Opcional para ver la representacion de las casillas con sus literales
# print(" Maze's literals", maze.get_maze_literals_representation(pretty=True), sep="\n")

print(" Maze Legend:")
print("  Starting Point:", M.USER)
print("           Walls:", M.WALL)
print("      Objectives:", M.FLAG)
print()
print(" Maze:", maze.get_maze_representation(pretty=True), sep="\n")

model = solver.get_model()
if model is not None:
  print(" Maze's possible solution:", maze.get_maze_representation_with_path(model, pretty=True), sep="\n")
else:
  print("    No Solution")


# Testing key position's clauses
# print(maze.get_route_conditions(8, 0), end="\n\n")
# print(maze.get_route_conditions(8, 1), end="\n\n")
# print(maze.get_route_conditions(8, 4), end="\n\n")
# print(maze.get_route_conditions(7, 4), end="\n\n")
