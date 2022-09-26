import sys
import json

from constants import *

f = open(sys.argv[1])
maxhs_solution = f.read()
f.close()

model = []
for i in range(1, len(maxhs_solution) + 1):
  model.append(i if maxhs_solution[i - 1] == "1" else -i)

f = open(OUTPUT_DIR + "maxhs_model.json", "w")
f.write(json.dumps(model))
f.close()
