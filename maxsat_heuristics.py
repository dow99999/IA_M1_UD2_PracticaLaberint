import json

from MazeSatDoubleTiles import MazeSatDoubleTiles


from pysat.formula import WCNF

from constants import GENERAL_TILE_WEIGHT

def maxsat_clauses_with_heuristic(wcnf: WCNF, maze: MazeSatDoubleTiles):
  flags = maze.get_element_literals(MazeSatDoubleTiles.FLAG)
  flags = [ maze.get_position_from_literal(x) for x in flags ]
  user = maze.get_position_from_literal(maze.get_element_literals(MazeSatDoubleTiles.USER)[0])
  maze_l = (maze.get_maze_width() * maze.get_maze_height())

  targets = [ user ] + flags
  
  targets_x = [ x[0] for x in targets ]
  targets_y = [ x[1] for x in targets ]

  # N, E, S, O
  rects = [
    min(targets_y),
    max(targets_x),
    max(targets_y),
    min(targets_x)
  ]

  representation = []

  for i in range(1, maze_l + 1):
    pos = maze.get_position_from_literal(i)
    weight = 1

    # Pesos por distancias a los objectivos
    for f in flags:
      weight += manhattan_distance(pos, f)

    out_multiplier = 0
    # Pesos por salir del rectangulo
    if pos[0] > rects[1]:
      out_multiplier += pos[0] - rects[1]
    if pos[0] < rects[3]:
      out_multiplier += rects[3] - pos[0]

    if pos[1] < rects[0]:
      out_multiplier += rects[0] - pos[1]
    if pos[1] > rects[2]:
      out_multiplier += pos[1] - rects[2]

    weight += out_multiplier * weight

    print(pos, weight)

    if len(representation) <= pos[0]:
      representation.append([])
    
    representation[pos[0]].append(weight)

    wcnf.append([-i], weight=weight)

  for i in representation:
    print(i)


def manhattan_distance(current, target):
  return abs(current[0] - target[0]) + abs(current[1] - target[1])