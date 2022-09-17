from pysat.solvers import Solver
from pysat.formula import CNF

s = Solver(name="cd")
cnf = CNF()

cnf.append([1, 2])
cnf.append([1, -2])

print(cnf.clauses)

s.append_formula(cnf)

print(s.solve(assumptions=[-1]))
