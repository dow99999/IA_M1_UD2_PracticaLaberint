from Maze import Maze
import itertools

import json

# elements = [1, 2, 3]

# print(Maze.combinations_generator(elements, 2))
# print([ x for x in itertools.combinations(elements, 2)])



a = dict()
b = dict()
c = dict()

a[0] = b
b[0] = c
c[0] = a


print(a)
