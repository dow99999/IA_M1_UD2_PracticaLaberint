from Maze import Maze

class MazeSat(Maze):
  """
  Clase para representar un laberinto y generar las clausulas necesarias para resolverlo
  """

  def __init__(self, matrix: list = None):
    super().__init__(matrix)



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
    
    # si estamos en la posicion del user o un flag estamos en un extremo del camino, por tanto no hay minimo 2
    if self._representation[row][col] == Maze.FLAG or self._representation[row][col] == Maze.USER:
      clauses.append(neighbours + [-target_literal]) # minimo un vecino
      
      # Restriccion menor o igual a 1
      combinations = Maze.combinations_generator(neighbours, 2)

      for c in combinations:
        aux = []
        for val in c:
          aux.append(-val)
        clauses.append(aux + [-target_literal])
    else:
      ###
      # Probablemente se puede generalizar esta zona ↓
      
      # Restriccion mayor o igual a 2: para ser un camino tiene que tener un lugar de donde viene y un lugar a donde va
      if len(neighbours) == 4:  # condiciones para casillas con 4 posibilidades
        for i in range(len(neighbours)):
          aux = []
          for n in neighbours:
            aux.append(-n if neighbours[i] == n else n)
          clauses.append(aux + [-target_literal])
      else: # condiciones para casillas con menos de 4 posibilidades
        d_comb = Maze.combinations_generator(neighbours, 2)
        for c in d_comb:
          aux = []
          for n in neighbours:
            aux.append(n if n in c else -n)
          clauses.append(aux + [-target_literal])
      
      # probablemente se puede generalizar esta zona ↑
      ###

      # Restriccion menor o igual a 2
      combinations = Maze.combinations_generator(neighbours, 3)

      for c in combinations:
        aux = []
        for val in c:
          aux.append(-val)
        clauses.append(aux + [-target_literal])


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
    clauses = []
    for wall in self.get_element_literals(Maze.WALL):
      clauses.append([-wall])

    return clauses

  def get_all_flags_clause(self):
    """
    Devuelve una clausula con los objetivos dentro del laberinto
    """
    flags = []
    for flag in self.get_element_literals(Maze.FLAG):
      flags.append(flag)
    
    return flags

  def get_user_clause(self):
    """
    Devuelve una clausula representando el usuario
    """
    return [self.get_element_literals(Maze.USER)[0]]