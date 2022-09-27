# Este script necesita maxcdcl_static
# No es muy fiable para tiempos pequenos, una sola ejecucion ya son 300ms aprox

import sys
import os
import time

from constants import *


args = ""
for i in range(1, len(sys.argv)):
  args += " " + sys.argv[i]

print("./maxcdcl_static" + args)

f_time = 0
for i in range(TEST_ITERATIONS):
  i_time = time.time_ns()
  os.system("./maxcdcl_static" + args)
  f_time += time.time_ns() - i_time

print("Solved", TEST_ITERATIONS, "iterations in", (f_time / 1000000) / 1000, "s")