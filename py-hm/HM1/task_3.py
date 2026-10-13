num_list = list(map(int, input().split()))
str_list = input().split() #доп. проверка со строкой

def setlist(num_list):
    res = []
    seen = set() 
    #множество даёт проверку num in seen за O(1), поэтому цикл O(n)
    #если бы мы взяли список, проверка была бы O(n) и весь алгоритм O(n**2)
    for num in num_list:
        if num not in seen:
            res.append(num)
            seen.add(num)
    return res

print(setlist(num_list))
print(setlist(str_list))