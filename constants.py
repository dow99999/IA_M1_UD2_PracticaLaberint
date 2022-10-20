from Maze import Maze as M

### Solver a utilizar
SOLVER_NAME = "cd"

# Iteraciones para las que se ejecutara el calculo de la solucion
TEST_ITERATIONS = 100

#####################################################################################################################
# Generacion de archivos de datos
###

# Guarda las clausulas generadas por un experimento en un archivo (clauses.cnf | clauses.wcnf)
SAVE_CLAUSES_TO_FILE = True

# Guarda el modelo que soluciona el experimento en un archivo .json (solution.json)
DUMP_MODEL_TO_FILE = True

# Guarda el output del programa en un archivo de texto (output.log)
SEND_OUTPUT_TO_FILE = False

# Guarda la representacion del laberinto solucionado en un archivo de imagen(solved_maze.png)
SAVE_MAZE_SOLUTION_TO_PNG = True

# Todos los archivos de salida se guardaran dentro de esta carpeta
OUTPUT_DIR = "./out_files/"



#####################################################################################################################
# Opciones de visualizacion de laberintos
###

# Mostrar el laberinto sin resolver
SHOW_MAZE_REPRESENTATION = False

# Mostrar los literales del laberinto
SHOW_LITERAL_REPRESENTATION = False

# Mostrar el laberinto resuelto
SHOW_MAZE_SOLUTION = False

# Mostrar la resolucion del laberinto separado por capas, en caso de que el experimento las use
SHOW_MAZE_LAYERED_SOLUTION = False



#####################################################################################################################
# Opciones de visualizacion de variables
###

# Muestra el numero total de clausulas generadas
SHOW_CLAUSE_NUMBER = True

# Muestra el tiempo empleado por el solver para resolver el problema
SHOW_SOLVING_TIME = True

# Muestra la longitud del camino
SHOW_PATH_LENGTH = True

# Muestra el coste de la solucion en caso de usar MaxSAT
SHOW_MODEL_COST = True


#####################################################################################################################
# Opciones de generacion de ciclos
###

# Fuerza un loop en el modelo
FORCE_LOOP = False          # Usando una casilla, para las resoluciones LAYERED
FORCE_LAYERED_LOOP = False  # Usando dos casillas, para las resoluciones DOUBLE_TILE
LOOP_TILE_WEIGHT = 1        # Peso de una casilla de generacion de ciclos, usado para las soluciones MaxSAT

# Peso general de crear una casilla, usado para las soluciones MaxSAT
GENERAL_TILE_WEIGHT = 2



#####################################################################################################################
# Configuracion general del programa
###

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
MAXSAT_WITH_HEURISTICS_MANUAL = "7"
MAXSAT_WITH_HEURISTICS_PYSAT = "8"

OPTIONS = [
  SAT_DOUBLE_TILE,
  SAT_DOUBLE_TILE_PYSAT_CARDINALITY,
  SAT_LAYERED_TILES,
  MAXSAT_DOUBLE_TILE,
  MAXSAT_DOUBLE_TILE_PYSAT_CARDINALITY,
  MAXSAT_LAYERED_TILES,
  MAXSAT_WITH_HEURISTICS_MANUAL,
  MAXSAT_WITH_HEURISTICS_PYSAT
  ]
#####################################

assert (not (FORCE_LOOP and FORCE_LAYERED_LOOP)), "Check constants, FORCE_LOOP and FORCE_LAYERED_LOOP can't be true at the same time"


#####################################################################################################################
# Datos especificos de la generacion de ciclos
###

# Aqui se pueden cambiar las casillas que generan un loop segun resolucion usada, ya estan colocadas para formar un ciclo con las distintas soluciones
LOOP_CLAUSES = []
if FORCE_LOOP:
  LOOP_CLAUSES = [[40], [39]]
if FORCE_LAYERED_LOOP:
  LOOP_CLAUSES = [[40]]
