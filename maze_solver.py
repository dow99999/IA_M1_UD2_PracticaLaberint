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
import time
import json

from pysat.solvers import Solver
from pysat.examples.rc2 import RC2
from pysat.formula import CNF, WCNF

# Para gestionar diferentes parametros del programa
from constants import *


if SEND_OUTPUT_TO_FILE:
  f = open(OUTPUT_DIR + 'output.log','w', encoding="utf-8")
  sys.stdout = f

if len(sys.argv) not in [2, 3] or sys.argv[1] not in OPTIONS:
  print("Needs one argument from this list ", [ int(o) for o in OPTIONS ],": ", sep="")
  print(" 1. (Working~) SAT Double Tiles Path With Manual Cardinality Restrictions")
  print(" 2. (Working) SAT Double Tiles Path With PySat Cardinality Restrictions")
  print(" 3. (Working~) SAT Layered One Direction Path\n")
  print(" 4. (Working) MaxSAT Double Tiles Path With Manual Cardinality Restrictions")
  print(" 5. (Working) MaxSAT Double Tiles Path With PySat Cardinality Restrictions")
  print(" 6. (Working) MaxSAT Layered One Direction Path")
  exit()

# Cargamos segun el tipo de resolucion que usaremos (DOUBLE_TILE o LAYERED)
if sys.argv[1] in [SAT_DOUBLE_TILE, SAT_DOUBLE_TILE_PYSAT_CARDINALITY, MAXSAT_DOUBLE_TILE, MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY]:
  from MazeSatDoubleTiles import MazeSatDoubleTiles as M
elif sys.argv[1] in [SAT_LAYERED_TILES, MAXSAT_LAYERED_TILES]:
  from MazeSatLayeredTiles import MazeSatLayeredTiles as M

# Comprovacion de si el experimento es de tipo MaxSAT o SAT
USING_MAXSAT = sys.argv[1] in [MAXSAT_DOUBLE_TILE, MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY, MAXSAT_LAYERED_TILES]

# Activar para seleccionar manualmente la direccion por donde empezara el camino
INTERACTIVE_DIRECTION = False

# en caso de usar DOUBLE_TILE gestionamos que tipo de restriccion de cardinalidad usaremos (manual o de pysat)
if sys.argv[1] in [SAT_DOUBLE_TILE, SAT_DOUBLE_TILE_PYSAT_CARDINALITY, MAXSAT_DOUBLE_TILE, MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY]:
  maze = M(pysat_cardinality=(sys.argv[1] in [SAT_DOUBLE_TILE_PYSAT_CARDINALITY, MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY]))
else:
  maze = M()

# Cargamos los datos de casilla del laberinto
if len(sys.argv) == 3:
  maze.load_maze_from_file(sys.argv[2])
else:
  maze.load_maze_from_matrix(MAZE_MATRIX)

multipurpose_cnf = WCNF() if USING_MAXSAT else CNF()

# leyenda de los caracteres usados para representar el laberinto
print(" Maze Legend:")
print("  Starting Point:", M.USER)
print("           Walls:", M.WALL)
print("      Objectives:", M.FLAG)
print()


###################################
# Usado solo en el primer experimento (SAT_DOUBLE_TILE) y en caso que el usuario tenga mas de una opcion en el primer estado del laberinto
starting_paths = None

if INTERACTIVE_DIRECTION:
  print(" Maze's literals", maze.get_maze_literals_on_path(pretty=True), sep="\n")
  starting_paths = maze.get_neighbour_literals(*maze.get_position_from_literal(maze.get_element_literals(M.USER)[0]))
  start = None
  while start not in starting_paths:
    print("Possible Directions :", starting_paths)
    try:
      start = int(input("Select starting user direction: "))
    except: pass
###################################


# Opcional para ver la representacion de las casillas con sus literales
if SHOW_LITERAL_REPRESENTATION:
  print(" Maze's literals:", maze.get_maze_literals_representation(pretty=True), sep="\n")

# Mostramos el laberinto sin resolver
if SHOW_MAZE_REPRESENTATION:
  print(f" Maze [{maze.get_maze_width()}x{maze.get_maze_height()}]:", maze.get_maze_representation(pretty=True), sep="\n")


# Preparamos las clausulas:

# Anadimos casillas forzadas en caso de querer generar un ciclo
if FORCE_LOOP or FORCE_LAYERED_LOOP:
  if USING_MAXSAT:
    multipurpose_cnf.extend(LOOP_CLAUSES, weights=[LOOP_TILE_WEIGHT] * len(LOOP_CLAUSES))
  else:
    multipurpose_cnf.extend(LOOP_CLAUSES)

# La posicion del usuario
multipurpose_cnf.extend(maze.get_user_clauses(start if starting_paths else None))

# Un muro del laberinto no es un camino valido
multipurpose_cnf.extend(maze.get_all_wall_clauses())

# Se quiere llegar a, como maximo, un objetivo
multipurpose_cnf.extend(maze.get_all_flags_clauses())

# Generamos las condiciones de cada casilla
multipurpose_cnf.extend(maze.get_all_maze_route_clauses())

# Asignamos un peso fijo a toda casilla en caso de usar MaxSAT
if USING_MAXSAT:
  maze_l = (maze.get_maze_width() * maze.get_maze_height())
  if sys.argv[1] in [SAT_LAYERED_TILES, MAXSAT_LAYERED_TILES]:  # Las resoluciones LAYERED tienen mas casillas
    multipurpose_cnf.extend([[-x] for x in range(1, (maze_l * maze.get_layers()) + 1)], weights=[GENERAL_TILE_WEIGHT] * (maze_l * maze.get_layers()))
  else:
    multipurpose_cnf.extend([[-x] for x in range(1, maze_l + 1)], weights=[GENERAL_TILE_WEIGHT] * maze_l)

if SAVE_CLAUSES_TO_FILE:
  multipurpose_cnf.to_file(OUTPUT_DIR + "clauses." + ("w" if USING_MAXSAT else "") + "cnf")


f_time = 0
for i in range(TEST_ITERATIONS):
  print(f"Processing iteration {i + 1}/{TEST_ITERATIONS}")

  i_time = time.time_ns()

  # Inicializamos el solver con las restricciones ya generadas
  solver = RC2(multipurpose_cnf, solver=SOLVER_NAME) if USING_MAXSAT else Solver(bootstrap_with=multipurpose_cnf, name=SOLVER_NAME, use_timer=True)

  # Resolvemos el laberinto y obtenemos el modelo, diferenciando entre una resolucion SAT y una MaxSAT:
  if not USING_MAXSAT:
    solver.solve()
    f_time += solver.time() * 1000000000    # Pasamos de segundos a nanosegundos para mantener una misma unidad
    model = solver.get_model()
  else:
    model = solver.compute()  # en caso de MaxSAT resolvemos aqui el laberinto
    f_time += time.time_ns() - i_time




if DUMP_MODEL_TO_FILE:
  model_f = open(OUTPUT_DIR + "model.json", "w")
  model_f.write(json.dumps(model))
  model_f.close()


if model is not None:
  # En caso de alguna resolucion LAYERED mostramos el camino en cada capa
  if SHOW_MAZE_LAYERED_SOLUTION and sys.argv[1] in [ SAT_LAYERED_TILES, MAXSAT_LAYERED_TILES ]:
    print("Maze's paths per layer:", maze.get_maze_layer_representation_with_path(model, pretty=True), sep="\n")
  
  if SHOW_MAZE_SOLUTION:
    print(" Maze's possible solution:", maze.get_maze_representation_with_path(model, pretty=True), sep="\n")
  
  if SAVE_MAZE_SOLUTION_TO_PNG:
    maze.save_solved_maze_to_image(model)
    print("Saved solved maze on " + OUTPUT_DIR + "solved_maze.png")

  # En caso de MaxSAT mostramos ademas el coste del camino
  if USING_MAXSAT and SHOW_MODEL_COST:
    print("Model cost:", solver.cost)

  if SHOW_PATH_LENGTH:
    # Contamos de todos los literales de casilla cuantos estan en positivo
    max_literal = (maze.get_maze_width() * maze.get_maze_height() * (maze.get_layers() if callable(getattr(maze, "get_layers", None)) else 1))
    print("Path length:", len([x for x in model if x > 0 and x <= max_literal]))
else:
  print("    No Solution")

# Mostramos el numero de clausulas usadas en la resolucion
if SHOW_CLAUSE_NUMBER:
  print("Number of clauses:", len(multipurpose_cnf.clauses) if type(multipurpose_cnf) is CNF else (len(multipurpose_cnf.hard) + len(multipurpose_cnf.soft)))

if SHOW_SOLVING_TIME:
  print("Solving time for " + str(TEST_ITERATIONS) + " iterations:", (f_time / 1000000) / 1000, "s")

# Testing key position's clauses
# print(maze.get_route_conditions(8, 0), end="\n\n")
# print(maze.get_route_conditions(8, 1), end="\n\n")
# print(maze.get_route_conditions(8, 4), end="\n\n")
# print(maze.get_route_conditions(7, 4), end="\n\n")

if SEND_OUTPUT_TO_FILE:
  f.close()