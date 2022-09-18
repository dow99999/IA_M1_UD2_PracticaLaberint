class Maze:
  PATH = " "
  WALL = "■"
  USER = "¤"
  FLAG = "ƒ"

  def combinations_generator(elements: list, length: int):
    combinations = []

    def generate(comb):
      if len(comb) == length:
        if comb not in combinations:
          combinations.append(comb)
        return
      
      for e in elements:
        if e not in comb:
          generate(comb | {e})
    
    generate(set())

    return [ list(x) for x in combinations ]

  def __init__(self, matrix: list = None):
    self.__representation = []
    self.__width = 0
    self.__height = 0

    if matrix != None:
      self.load_maze_from_matrix(matrix)

  def _box_maze(self, representation: str):
    out = ""
    lines = representation.split("\n")

    out += "┌" + ("─" * (len(lines[0]) + 1)) + "┐\n"

    for line in lines:
      if line != "":
        out += "│ "
        for c in line:
          out += c
        out += "│\n"

    out += "└" + ("─" * (len(lines[0]) + 1)) + "┘"

    return out


  def load_maze_from_matrix(self, matrix: list):
    self.__representation = matrix.copy()
    self.__width = len(self.__representation[0])
    self.__height = len(self.__representation)

  def get_maze_matrix(self):
    return self.__representation.copy()

  def get_maze_height(self):
    return self.__height
    
  def get_maze_width(self):
    return self.__width

  def get_maze_representation_with_path(self, model: list, pretty: bool = False):
    out = ""
    model_i = 1

    for row in self.__representation:
      for element in row:
        out += ("·" if model_i in model else element) + " "
        model_i += 1
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)
  
  def get_maze_representation(self, pretty: bool = False):
    out = ""

    for row in self.__representation:
      for element in row:
        out += element + " "
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)

  def get_maze_literals_representation(self, pretty: bool = False):
    out = ""
    current_literal = 1

    for row in self.__representation:
      for element in row:
        if current_literal < 10: out += " "
        out += str(current_literal) + " "
        current_literal += 1
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)

  def modify_element(self, row: int, col: int, new_element: str):
    self.__representation[row][col] = new_element
  
  def get_literal_from_position(self, row: int, col: int):
    return col + (self.__width * row) + 1

  def get_position_from_literal(self, literal: int):
    literal -= 1
    return (literal // self.__width, literal % self.__width)



  def get_element_literals(self, target: str):
    literals = []
    current_literal = 1

    for row in self.__representation:
      for element in row:
        if element == target:
          literals.append(current_literal)
        current_literal += 1

    return literals


  def get_neighbour_literals(self, row: int, col: int):
    literals = []

    if row > 0:
      literals.append(self.get_literal_from_position(row - 1, col))
    if col > 0:
      literals.append(self.get_literal_from_position(row, col - 1))
    if col < self.__width - 1:
      literals.append(self.get_literal_from_position(row, col + 1))
    if row < self.__height - 1:
      literals.append(self.get_literal_from_position(row + 1, col))

    return literals

  def get_route_conditions(self, row: int, col: int):
    neighbours = self.get_neighbour_literals(row, col)
    target_literal = self.get_literal_from_position(row, col)
    clauses = []
    
    # si estamos en la posicion del user o un flag estamos en un extremo del camino, por tanto no hay minimo 2
    if self.__representation[row][col] == Maze.FLAG or self.__representation[row][col] == Maze.USER:
      clauses.append(neighbours + [-target_literal]) # minimo un vecino
      
      # Restriccion menor o igual a 1
      combinations = Maze.combinations_generator(neighbours, 2)

      for c in combinations:
        aux = []
        for val in c:
          aux.append(-val)
        clauses.append(aux + [-target_literal])
    else:
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
      
      # Restriccion menor o igual a 2
      combinations = Maze.combinations_generator(neighbours, 3)

      for c in combinations:
        aux = []
        for val in c:
          aux.append(-val)
        clauses.append(aux + [-target_literal])


    return clauses

  def get_all_maze_route_conditions(self):
    clauses = []
    for row_i in range(self.__height):
      for col_i in range(self.__width):
        clauses += self.get_route_conditions(row_i, col_i)
    return clauses
