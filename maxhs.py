# Este script necesita maxhs
# El script utiliza python3

import sys
import subprocess
import os

from constants import *

def decode_output(output: list):
  for i in range(len(output)):
    output[i] = output[i].decode("utf-8")

def get_line_starting_with(output: list, target: str):
  for i in range(len(output) - 1, -1, -1):
    if output[i].startswith(target):
      return output[i]

def get_model_solution(output: list):
  line = get_line_starting_with(output, "v ")
  return line.split(" ")[1]

def get_model_solving_time(output: list):
  line = get_line_starting_with(output, "c CPU")

  return float((line.split(":")[1]).split(" ")[1])



args = []
for i in range(1, len(sys.argv)):
  args.append(sys.argv[i])

f_time = 0
for i in range(TEST_ITERATIONS):
  print(f"Processing iteration {i + 1}/{TEST_ITERATIONS}")
  output = subprocess.check_output(["./maxhs", "-printSoln"] + args)
  output = output.splitlines(keepends=False)
  decode_output(output)

  f_time += get_model_solving_time(output)

with open(OUTPUT_DIR + "maxhs.temp", "w") as f:
  f.write(get_model_solution(output))
  f.close()

os.system("python3 maxsat_model_parser.py " + OUTPUT_DIR + "/maxhs.temp")

os.remove(OUTPUT_DIR + "maxhs.temp")



print("Solved", TEST_ITERATIONS, "iterations in", f_time, "s")