row1, col1 = int(input()), int(input())
row2, col2 = int(input()), int(input())

def horse_moves(row, col):
    moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    return sorted((row+dr, col+dc) for dr, dc in moves if (0 <= row+dr < 8) and (0 <= col+dc < 8))

def can_move(start, end):
    return end in horse_moves(*start)

print(horse_moves(row1, col1))
print(can_move((row1, col1), (row2,col2)))