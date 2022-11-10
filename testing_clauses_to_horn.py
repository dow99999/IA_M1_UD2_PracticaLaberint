clauses = [
  [1, 2, 3],
  [-1, 2, 4],
  [-1],
  [-2],
  [-3],
  [2, 3, 4],
  [3, 4, -5, -6, -7]
]

final_clauses = []

for c in clauses:
  aux = []
  for l in c:
    aux.append(-l)
  final_clauses.append(aux)


print(clauses)


final_clauses = list(final_clauses)

final_clauses.sort()

print(final_clauses)
