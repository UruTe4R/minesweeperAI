my_set = {(1, 2), (1, 1), (2, 3), (1, 3), (3, 4)}

sorted_set = sorted(my_set, key=lambda x: (x[0], x[1]))
print(sorted_set)