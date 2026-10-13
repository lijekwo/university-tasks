a, b = int(input()), int(input())

def sum_num(n):
    s = 0
    while n > 0:
        s += n%10
        n //= 10
    return s

def mul_num(n):
    s = 1
    while n > 0:
        digit = n%10
        if digit!=0:
            s*= digit
        n //= 10
    return s 

def equal(a,b):
    if a < 0 or b < 0:
        print('Нельзя отрицательные')
        return []
    else:
        res = []
        for i in range(a,b+1):
            if sum_num(i) == mul_num(i):
                res.append(i)
        return res

res = equal(a,b)
print(*res)
print(len(res)) 
