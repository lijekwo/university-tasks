count = 0
total = 0
minimum = None
maximum = None

with open("numbers.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        number = int(line)

        count += 1
        total += number

        if minimum is None or number < minimum:
            minimum = number
        if maximum is None or number > maximum:
            maximum = number

if count > 0:
    print("Количество:", count)
    print("Сумма:", total)
    print("Минимум:", minimum)
    print("Максимум:", maximum)
    print("Среднее:", total / count)
else:
    print("В файле нет чисел")