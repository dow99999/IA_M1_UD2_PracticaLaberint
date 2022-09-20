from Maze import Maze

from pysat import card
from pysat.formula import IDPool


class MazeSat(Maze):
  """
  Clase para representar un laberinto y generar las clausulas necesarias para resolverlo.
  Esta resolucion utiliza las reglas explicadas en la practica
  """

  def __init__(self, matrix: list = None):
    super().__init__(matrix)

    self.__idpool = IDPool(occupied=[[1, self._height * self._width]])


  #######################################################################
  ## Maze Representations
  #######################################################################

  def get_maze_literals_representation(self, pretty: bool = False):
    """
    Devuelve un string con la representacion del laberinto en literales
    """
    out = ""
    current_literal = 1

    for row in self._representation:
      for element in row:
        if current_literal < 10: out += " "
        out += str(current_literal) + " "
        current_literal += 1
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)

  def get_maze_literals_on_path(self, pretty: bool = False):
    """
    Devuelve un string con la representacion del laberinto y los literales del camino
    """
    out = ""
    current_literal = 1

    for row in self._representation:
      for element in row:
        if element == Maze.PATH:
          if current_literal < 10: out += " "
          out += str(current_literal) + " "
        else:
          out += element + "  "
        current_literal += 1
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)

  def get_maze_representation_with_path(self, model: list, pretty: bool = False):
    """
    Devuelve un string con la misma representacion de laberinto que get_maze_representation pero con
    el camino definido por model marcado por puntos
    """
    out = ""
    model_i = 1

    for row in self._representation:
      for element in row:
        out += (Maze.WAY if model_i in model else element) + " "
        model_i += 1
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)






  #######################################################################
  ## Transformations
  #######################################################################

  def get_literal_from_position(self, row: int, col: int):
    """
    Devuelve un literal dadas las coordenadas de una casilla
    """
    return col + (self._width * row) + 1

  def get_position_from_literal(self, literal: int):
    """
    Devuelve las coordenadas de una casilla dado un literal
    """
    literal -= 1
    return (literal // self._width, literal % self._width)

  def get_element_literals(self, target: str):
    """
    Devuelve una lista de todos los literales de un tipo
    """
    literals = []
    current_literal = 1

    for row in self._representation:
      for element in row:
        if element == target:
          literals.append(current_literal)
        current_literal += 1

    return literals






  #######################################################################
  ## Clause generators
  #######################################################################

  def get_neighbour_literals(self, row: int, col: int):
    """
    Devuelve una lista de los literales conectados a una casilla, dicho de otro modo, los literales con los cuales 
    se puede formar un camino a traves de la casilla
    """
    literals = []

    if row > 0:
      literals.append(self.get_literal_from_position(row - 1, col))
    if col > 0:
      literals.append(self.get_literal_from_position(row, col - 1))
    if col < self._width - 1:
      literals.append(self.get_literal_from_position(row, col + 1))
    if row < self._height - 1:
      literals.append(self.get_literal_from_position(row + 1, col))

    return literals

  def get_route_conditions(self, row: int, col: int):
    """
    Devuelve una lista de clausulas que definen el camino posible a traves de una casilla
    """
    neighbours = self.get_neighbour_literals(row, col)
    target_literal = self.get_literal_from_position(row, col)
    clauses = []

    if self._representation[row][col] != Maze.FLAG:
      clauses.extend([
        clause + [ -target_literal ] for clause in 
        card.CardEnc.equals(
          lits= neighbours,
          bound=1,
          vpool=self.__idpool,
          encoding=card.EncType.pairwise
        ).clauses
      ])

    # ir por estados y ejecutar el solver en cada estado? no se me ocurre otra forma

    return clauses

  def get_all_maze_route_clauses(self):
    """
    Devuelve una lista de clausulas que definen el camino posible entre todas las casillas
    """
    clauses = []
    for row_i in range(self._height):
      for col_i in range(self._width):
        clauses += self.get_route_conditions(row_i, col_i)
    return clauses

  def get_all_wall_clauses(self):
    """
    Devuelve una lista de clausulas que definen las casillas con muros
    """
    return [[-wall] for wall in self.get_element_literals(Maze.WALL)]

  def get_all_flags_clauses(self):
    """
    Devuelve una clausula con los objetivos dentro del laberinto
    """
    
    return card.CardEnc.equals(
      lits=self.get_element_literals(Maze.FLAG),
      bound=1,
      vpool=self.__idpool,
      encoding=card.EncType.pairwise
    ).clauses

  def get_user_clauses(self, force_direction=None):
    """
    Devuelve una clausula representando el usuario, opcionalmente se puede pasar un literal para
    forzar una direccion hacia la que empezar el camino
    """
    out = [[self.get_element_literals(Maze.USER)[0]]]
    if force_direction: out.append([force_direction])

    return out