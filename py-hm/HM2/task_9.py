import re
def parse_number(value):
    if re.fullmatch(r"-?\d+(\.?\d+)?", value):
        return float(value)
    raise ValueError('Строка неверного формата')
m = input()
try:
    print(parse_number(m))
except TypeError as e:
    print(f"Получена ошибка типа {e}")
except ValueError as e:
    print(f"Получена ошибка значения {e}")