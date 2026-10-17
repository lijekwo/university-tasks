import csv

students_count = 0
students_sum = 0
max_score = -1
best_student = None
group_score = {}

with open('students.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)

    for row in reader:
        name, group, score = row[0], row[1], int(row[2])

        students_count += 1
        students_sum += score

        if score > max_score:
            max_score = score
            best_student = name

        if group not in group_score:
            group_score[group] = [1, score]
        else:
            group_score[group][0] += 1
            group_score[group][1] += score

print("Средний балл всех:", round(students_sum / students_count, 2))
print("Лучший студент:", best_student, max_score)

for group, (count, total) in group_score.items():
    print("Группа", group, "— средний балл:", round(total / count, 2))