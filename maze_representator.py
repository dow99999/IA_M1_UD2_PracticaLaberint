import sys
import json

from constants import *

if len(sys.argv) not in [3, 4]:
  print("usage: maze_representator.py <maze_algorithm_id> <model_path> [maze_path]")
  print("Maze Algorithms:")
  print(" 1. Double Tiles")
  print(" 2. Layered Tiles")
  exit()

model_f = open(sys.argv[2], "r")
model = json.loads(str(model_f.read()))
model_f.close()


if sys.argv[1] == "1":
  from MazeSatDoubleTiles import MazeSatDoubleTiles as M
elif sys.argv[1] == "2":
  from MazeSatLayeredTiles import MazeSatLayeredTiles as M

maze = M()


if len(sys.argv) == 4:
  maze.load_maze_from_file(sys.argv[3])
else:
  maze.load_maze_from_matrix(MAZE_MATRIX)


if SHOW_MAZE_SOLUTION:
  print(maze.get_maze_representation_with_path(model, pretty=True))

if True:
  maze.save_solved_maze_to_image(model)
  print("Saved solved maze on " + OUTPUT_DIR + "solved_maze.png")