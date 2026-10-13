import math
import numpy as np 

def linear_regression(x, y):
    if min(x) == max(x):
        raise ValueError("Все значения х одинаковы")

    n = len(x)
    mean_x = sum(x)/n
    mean_y = sum(y)/n

    a = sum((xi - mean_x) * (yi - mean_y) for xi,yi in zip(x,y)) \
    / sum( (xi - mean_x) ** 2 for xi in x)
    b = mean_y - a * mean_x
    return a,b

def linear_regression_numpy(x,y):
    if min(x) == max(x):
        raise ValueError("Все значения х одинаковы")

    a,b = np.polyfit(x,y,1)
    return float(a), float(b)

def predict(a,b,x_new):
    return a * x_new + b

x  = list(map(float, input('Введите значения x: ').split()))
y  = list(map(float, input('Введите значения y: ').split()))

try:
    a1,b1 = linear_regression(x,y)
    a2,b2 = linear_regression_numpy(x,y)

    print(f'Без numpy: a = {a1}, b = {b1}')
    print(f'С numpy: a = {a2}, b = {b2}')

    x_new = float(input('Введите новый x для предсказания: '))
    
except ValueError as e:
    print('Ошибка',e)