my_set = {(1, 2), (1, 1), (2, 3), (1, 3), (3, 4)}
knowledge = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

count = 0
print(len(knowledge))
for i, s1 in enumerate(knowledge):
  for j in range(i + 1, len(knowledge)):
    s2 = knowledge[j]
    print(i, j)
    print(s1, s2)
    count += 1

print(count)