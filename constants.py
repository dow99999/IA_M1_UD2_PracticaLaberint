from Maze import Maze as M

# Solver a utilizar
SOLVER_NAME = "g4" 

# Mostrar los literales del laberinto
SHOW_LITERAL_REPRESENTATION = False

# Muestra el numero total de clausulas generadas
SHOW_CLAUSE_NUMBER = True

# Muestra la longitud del camino
SHOW_PATH_LENGTH = True

# Muestra el coste de la solucion en caso de usar MaxSAT
SHOW_MODEL_COST = True

# Fuerza un loop en el modelo
FORCE_LOOP = False          # Usando una casilla, para las resoluciones LAYERED
FORCE_LAYERED_LOOP = False  # Usando dos casillas, para las resoluciones DOUBLE_TILE
LOOP_TILE_WEIGHT = 1        # Recomendado usar una weight menor a la de generar una casilla

# Peso general de crear una casilla, usado para las soluciones MaxSAT
GENERAL_TILE_WEIGHT = 2

# Representacion del laberinto en una matriz por tipos
MAZE_MATRIX = [
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

#####################################
# Lista de experimentos
SAT_DOUBLE_TILE = "1"
SAT_DOUBLE_TILE_PYSAT_CARDINALITY = "2"
SAT_LAYERED_TILES = "3"
MAXSAT_DOUBLE_TILE = "4"
MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY = "5"
MAXSAT_LAYERED_TILES = "6"

OPTIONS = [
  SAT_DOUBLE_TILE,
  SAT_DOUBLE_TILE_PYSAT_CARDINALITY,
  SAT_LAYERED_TILES,
  MAXSAT_DOUBLE_TILE,
  MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY,
  MAXSAT_LAYERED_TILES
  ]
#####################################

assert (not (FORCE_LOOP and FORCE_LAYERED_LOOP)), "Check constants, FORCE_LOOP and FORCE_LAYERED_LOOP can't be true at the same time"

# Aqui se pueden cambiar las casillas que generan un loop segun resolucion usada, ya estan colocadas para formar un ciclo con las distintas soluciones
LOOP_CLAUSES = []
if FORCE_LOOP:
  LOOP_CLAUSES = [[40], [39]]
if FORCE_LAYERED_LOOP:
  LOOP_CLAUSES = [[40]]