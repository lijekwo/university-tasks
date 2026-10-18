import re

with open("text.txt", encoding="utf-8") as file:
    text = file.read()

emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)

for email in dict.fromkeys(emails):
    print(email)