class Labyrinth:
  PATH = " "
  WALL = "x"
  USER = "u"
  FLAG = "o"

  def __init__(self):
    self.__representation = []
    self.__width = 0
    self.__height = 0

  def load_labyrinth_from_matrix(self, matrix: list):
    self.__representation = matrix.copy()
    self.__width = len(self.__representation[0])
    self.__height = len(self.__representation)

  def get_labyrinth_matrix(self):
    return self.__representation.copy()

  def get_labyrinth_representation(self):
    out = ""

    for row in self.__representation:
      for element in row:
        out += element + " "
      out += "\n"

    return out

  def get_labyrinth_literals_representation(self):
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
