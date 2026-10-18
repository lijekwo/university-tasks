import re
from collections import Counter

pattern = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARNING|ERROR)\b(?:.*?User (\d+))?"
)

levels = Counter()
error_users = set()

with open("logs.txt", encoding="utf-8") as file:
    for line in file:
        match = pattern.match(line)
        if not match:
            continue

        level, user_id = match.groups()
        levels[level] += 1

        if level == "ERROR" and user_id:
            error_users.add(user_id)

for level in ("INFO", "WARNING", "ERROR"):
    print(f"{level}: {levels[level]}")

print("Пользователи с ошибками:", ", ".join(sorted(error_users, key=int)))