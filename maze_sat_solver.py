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

from Maze import Maze as M

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

solver = Solver(name="g4")
cnf = CNF()

# Donde esta el usuario es por donde empezamos el camino
# Importante: En caso que el usuario tenga mas de una opcion para empezar el camino hay que forzar una direccion manualmente (con assumptions, por ejemplo)
cnf.append([maze.get_element_literals(M.USER)[0]])


# Un muro del laberinto no es un camino valido
for wall in maze.get_element_literals(M.WALL):
  cnf.append([-wall])

# Se quiere llegar al menos a un objetivo
flags = []
for flag in maze.get_element_literals(M.FLAG):
  flags.append(flag)
cnf.append(flags)


# Desde una posicion cualquiera se puede generar un solo camino de salida arriba, abajo, a la izquierda o la derecha
cnf.extend(maze.get_all_maze_route_conditions())

# print(cnf.clauses)

solver.append_formula(cnf)

solver.solve()
# print(solver.get_core())

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
