import re

user_ids = []
error_lines = []
error_user_ids = []

with open("logs.txt", encoding="utf-8") as file:
    for line in file:
        line = line.rstrip("\n")

        match = re.search(r"User (\d+)", line)
        if match:
            user_ids.append(match.group(1))

        if re.match(r"ERROR\b", line):
            error_lines.append(line)
            if match:
                error_user_ids.append(match.group(1))

print("Все идентификаторы пользователей:", user_ids)

print("Строки с ERROR:")
for line in error_lines:
    print(" ", line)

print("Пользователи с ошибками:", error_user_ids)