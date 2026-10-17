import json

with open("students.json", "r", encoding="utf-8") as file:
    students_data = json.load(file)

for student in students_data:
    student["passed"] = student["score"] >= 60

best = max(students_data, key=lambda s: s["score"])
print("Лучший студент:", best["name"], best["score"])

with open("new_students.json", "w", encoding="utf-8") as file:
    json.dump(students_data, file, indent=4, ensure_ascii=False)