class Maze:
  """
  Clase para representar un laberinto
  """

  # Representaciones de cada tipo de casilla
  PATH = " "
  WALL = "■"
  USER = "¤"
  FLAG = "ƒ"
  WAY = "·"
  

  def combinations_generator(elements: list, length: int):
    """
    Devuelve una lista con todas las combinaciones sin repeticiones de length longitud posibles de todos los elementos de elements
    """
    combinations = []

    # Hacemos todas las combinaciones posibles de elementos
    def generate(comb):
      if len(comb) == length:
        if comb not in combinations:
          combinations.append(comb) # Anadimos una combinacion solo si no ha sido anadida ya
        return
      
      for e in elements:
        if e not in comb:
          generate(comb | {e})
    
    generate(set())

    return [ list(x) for x in combinations ]  # Convertimos los sets en listas

  def __init__(self, matrix: list = None):
    self._representation = []
    self._width = 0
    self._height = 0

    if matrix != None:
      self.load_maze_from_matrix(matrix)

  def load_maze_from_matrix(self, matrix: list):
    """
    Carga una matriz de tipos de casilla en el objeto Maze
    """
    self._representation = matrix.copy()
    self._width = len(self._representation[0])
    self._height = len(self._representation)


  def _box_maze(self, representation: str):
    """
    Funcion interna para representar lineas de un string de misma longitud dentro de un recuadro
    """
    out = ""
    lines = representation.split("\n")

    out += "┌" + ("─" * (len(lines[0]) + 1)) + "┐\n"

    for line in lines:
      out += "│ "
      for c in line:
        out += c
      out += "│\n"

    out += "└" + ("─" * (len(lines[0]) + 1)) + "┘"

    return out


  def get_maze_matrix(self):
    """
    Devuelve la matriz de tipos de casilla del objeto
    """
    return self._representation.copy()

  def get_maze_height(self):
    """
    Devuelve la altura del laberinto
    """
    return self._height
    
  def get_maze_width(self):
    """
    Devuelve el ancho del laberinto
    """
    return self._width
  
  def get_maze_representation(self, pretty: bool = False):
    """
    Devuelve un string con la representacion del laberinto con un simbolo por tipo de casilla
    Ver las constantes estaticas de Maze para saber los tipos de casilla y su representacion
    """
    out = ""

    for row in self._representation:
      for element in row:
        out += element + " "
      out += "\n"

    out = out[:-1]

    return out if not pretty else self._box_maze(out)



  def modify_element(self, row: int, col: int, new_element: str):
    """
    Modifica el tipo de una casilla
    """
    self._representation[row][col] = new_element


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