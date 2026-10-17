with open("text.txt", encoding="utf-8") as file:
    lines = 0
    words = 0
    symbols = 0
    max_len = 0

    for line in file:
        lines += 1
        words += len(line.split())
        symbols += len(line)

        if len(line) > max_len:
            max_len = len(line)

print("Строк:", lines)
print("Слов:", words)
print("Символов:", symbols)
print("Самая длинная строка:", max_len)