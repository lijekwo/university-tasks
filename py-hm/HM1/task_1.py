n = int(input())
k = int(input())

def triangle(n):
    res = []

    for i in range(n):
        if i == 0:
            row = [1]
        else:
            prev_row = res[-1]
            row = [1]
            for j in range(len(prev_row)-1):
                row.append(prev_row[j] + prev_row[j+1])
            row.append(1)
        res.append(row)
    return res

def row_k(k):
    if k < 0:
        return []
    return triangle(k+1)[-1]

for row in triangle(n):
    print(*row)

print(*row_k(k))