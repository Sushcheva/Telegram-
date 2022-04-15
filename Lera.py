n = input().split()
for el in n:
    for i in n:
        if i != el:
            for j in n:
                if j != i and j != el:
                    print(el + ' ' + i + ' ' + j)
