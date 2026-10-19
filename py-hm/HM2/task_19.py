import re

text = input("Введите текст: ")

pattern = r"(?:\+7|8) (?:\(\d{3}\)|\d{3}) \d{3}-\d{2}-\d{2}"
phones = re.findall(pattern, text)

for phone in phones:
    print(phone)