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

import sys
from unicodedata import name

from pysat.solvers import Solver
from pysat.examples import rc2
from pysat.formula import CNF, WCNF

SAT_DOUBLE_TILE = "1"
SAT_DOUBLE_TILE_PYSAT_CARDINALITY = "2"
SAT_LAYERED_TILES = "3"

OPTIONS = [
  SAT_DOUBLE_TILE,
  SAT_DOUBLE_TILE_PYSAT_CARDINALITY,
  SAT_LAYERED_TILES
  ]

if len(sys.argv) != 2 or sys.argv[1] not in OPTIONS:
  print("Needs one argument from this list ", [ int(o) for o in OPTIONS ],": ", sep="")
  print(" 1. SAT Double Tiles Path With Manual Cardinality Restrictions")
  print(" 2. SAT Double Tiles Path With PySat Cardinality Restrictions")
  print(" 3. SAT Layered One Direction Path")
  exit()


if sys.argv[1] == "1" or sys.argv[1] == "2":
  from MazeSatDoubleTiles import MazeSatDoubleTiles as M
elif sys.argv[1] == "3":
  from MazeSatLayeredTiles import MazeSatLayeredTiles as M

USING_MAXSAT = sys.argv[1] not in [SAT_DOUBLE_TILE, SAT_DOUBLE_TILE_PYSAT_CARDINALITY, SAT_LAYERED_TILES]

# Activar para seleccionar manualmente la direccion por donde empezara el camino
INTERACTIVE_DIRECTION = False

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

if sys.argv[1] == "1" or sys.argv[1] == "2":
  maze = M(pysat_cardinality=(sys.argv[1] == "2"))
else:
  maze = M()
  
maze.load_maze_from_matrix(maze_matrix)

solver = rc2(name="g4") if USING_MAXSAT else Solver(name="g4")  # usamos Glucose4
multipurpose_cnf = WCNF() if USING_MAXSAT else CNF()


# Preparamos las clausulas:

# Donde esta el usuario es por donde empezamos el camino
# Importante: En caso que el usuario tenga mas de una opcion para empezar el camino hay que forzar una direccion manualmente

starting_paths = None

print(" Maze Legend:")
print("  Starting Point:", M.USER)
print("           Walls:", M.WALL)
print("      Objectives:", M.FLAG)
print()


if INTERACTIVE_DIRECTION:
  print(" Maze's literals", maze.get_maze_literals_on_path(pretty=True), sep="\n")
  starting_paths = maze.get_neighbour_literals(*maze.get_position_from_literal(maze.get_element_literals(M.USER)[0]))
  start = None
  while start not in starting_paths:
    print("Possible Directions :", starting_paths)
    try:
      start = int(input("Select starting user direction: "))
    except: pass



multipurpose_cnf.extend(maze.get_user_clauses(start if starting_paths else None))

# Un muro del laberinto no es un camino valido
multipurpose_cnf.extend(maze.get_all_wall_clauses())

# Se quiere llegar al menos a un objetivo
multipurpose_cnf.extend(maze.get_all_flags_clauses())

# Desde una posicion cualquiera se puede generar una o dos posiciones libres dependiendo de si se esta en el inicio del camino o en medio
route_clauses = maze.get_all_maze_route_clauses()
multipurpose_cnf.extend(route_clauses)

# print(cnf.clauses)
print("Number of Clauses:", len(multipurpose_cnf.clauses))

solver.append_formula(multipurpose_cnf)

# Resolvemos el laberinto:
solver.solve()
# print(solver.get_core())

# Opcional para ver la representacion de las casillas con sus literales
# print(" Maze's literals", maze.get_maze_literals_representation(pretty=True), sep="\n")

print(" Maze:", maze.get_maze_representation(pretty=True), sep="\n")

model = solver.get_model()
# print([x for x in model if x > 0])

if model is not None:
  if sys.argv[1] == SAT_LAYERED_TILES:
    print("Maze's paths per layer:", maze.get_maze_layer_representation_with_path(model, pretty=True), sep="\n")
  print(" Maze's possible solution:", maze.get_maze_representation_with_path(model, pretty=True), sep="\n")
else:
  print("    No Solution")


# Testing key position's clauses
# print(maze.get_route_conditions(8, 0), end="\n\n")
# print(maze.get_route_conditions(8, 1), end="\n\n")
# print(maze.get_route_conditions(8, 4), end="\n\n")
# print(maze.get_route_conditions(7, 4), end="\n\n")
