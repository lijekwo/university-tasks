count = 0
total = 0
minimum = None
maximum = None

with open("numbers.txt", encoding="utf-8") as file:
    for line in file:
        try:
            number = int(line)
        except ValueError:
            print("Ошибка:", line.strip())
            continue

        count += 1
        total += number

        if minimum is None or number < minimum:
            minimum = number
        if maximum is None or number > maximum:
            maximum = number

if count > 0:
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"Минимум: {minimum}\n")
        file.write(f"Максимум: {maximum}\n")
        file.write(f"Среднее: {total / count}")