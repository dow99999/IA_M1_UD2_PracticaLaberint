import sys
import json

from constants import *
from MazeSatDoubleTiles import MazeSatDoubleTiles as M

if len(sys.argv) not in [2, 3]:
  print("usage: maze_representator.py <model_path> [maze_path]")
  exit()

model_f = open(sys.argv[1], "r")
model = json.loads(str(model_f.read()))
model_f.close()

maze = M()
if len(sys.argv) == 3:
  maze.load_maze_from_file(sys.argv[2])
else:
  maze.load_maze_from_matrix(MAZE_MATRIX)

print(maze.get_maze_representation_with_path(model, pretty=True))
