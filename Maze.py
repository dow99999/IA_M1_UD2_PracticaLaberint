class Maze:
  PATH = " "
  WALL = "x"
  USER = "u"
  FLAG = "o"

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

  def get_maze_representation_with_path(self, model: list):
    out = ""
    model_i = 1

    for row in self.__representation:
      for element in row:
        out += ("·" if model_i in model else element) + " "
        model_i += 1
      out += "\n"

    return out
  
  def get_maze_representation(self):
    out = ""

    for row in self.__representation:
      for element in row:
        out += element + " "
      out += "\n"

    return out

  def get_maze_literals_representation(self):
    out = ""
    current_literal = 1

    for row in self.__representation:
      for element in row:
        out += str(current_literal) + " "
        current_literal += 1
      out += "\n"

    return out

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
    
    # clauses.append(neighbours + [-target_literal]) # minimo 1
    
    # Restriccion mayor o igual a 2
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
