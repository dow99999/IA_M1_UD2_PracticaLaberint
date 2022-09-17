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

from Labyrinth import Labyrinth as L

labyrinth_matrix = [
  [ L.FLAG, L.WALL, L.WALL, L.WALL, L.WALL, L.WALL, L.WALL, L.FLAG ],
  [ L.PATH, L.PATH, L.PATH, L.PATH, L.WALL, L.PATH, L.PATH, L.PATH ],
  [ L.PATH, L.WALL, L.WALL, L.PATH, L.WALL, L.PATH, L.WALL, L.PATH ],
  [ L.PATH, L.PATH, L.WALL, L.PATH, L.WALL, L.PATH, L.WALL, L.PATH ],
  [ L.WALL, L.PATH, L.WALL, L.PATH, L.PATH, L.PATH, L.PATH, L.PATH ],
  [ L.WALL, L.PATH, L.WALL, L.WALL, L.WALL, L.WALL, L.WALL, L.WALL ],
  [ L.PATH, L.PATH, L.PATH, L.PATH, L.PATH, L.PATH, L.PATH, L.PATH ],
  [ L.WALL, L.WALL, L.WALL, L.WALL, L.PATH, L.WALL, L.WALL, L.WALL ],
  [ L.USER, L.PATH, L.PATH, L.PATH, L.PATH, L.WALL, L.PATH, L.PATH ]
]

labyrinth = L()
labyrinth.load_labyrinth_from_matrix(labyrinth_matrix)

solver = Solver(name="cd")
cnf = CNF()

# Donde esta el usuario es por donde empezamos el camino
for user in labyrinth.get_element_literals(L.USER):
  cnf.append([user])

# Un muro del laberinto no es un camino valido
for wall in labyrinth.get_element_literals(L.WALL):
  cnf.append([-1*wall])

# Se quiere llegar al menos a un objetivo
flags = []
for flag in labyrinth.get_element_literals(L.FLAG):
  flags.append(flag)
cnf.append(flags)

# Desde una posicion cualquiera se puede generar un solo camino de salida arriba, abajo, a la izquierda o la derecha


# TODO: movimiento entre casillas


solver.append_formula(cnf)
print(solver.solve())