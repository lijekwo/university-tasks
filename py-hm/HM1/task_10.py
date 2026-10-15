import abc
import functools
import itertools
import json
import time


def timed(func):
    """Декоратор: измеряет, сколько секунд работала проверка"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        result.elapsed = time.perf_counter() - start
        return result

    return wrapper


class BaseChecker(abc.ABC):
    """Общий интерфейс для всех видов проверки"""

    @abc.abstractmethod
    def check(self, assignment, answer):
        """Возвращает долю правильности: число от 0 до 1"""


class NumericChecker(BaseChecker):
    """Числовая проверка: ответ должен совпасть с эталоном с допуском"""

    def __init__(self, tolerance=0.0):
        self.tolerance = tolerance

    def check(self, assignment, answer):
        try:
            value = float(str(answer).replace(",", "."))
        except ValueError:
            return 0.0
        correct = float(assignment.correct_answer)
        return 1.0 if abs(value - correct) <= self.tolerance else 0.0


class TextChecker(BaseChecker):
    """Текстовая проверка: сравнение строк без учёта регистра и пробелов по краям"""

    def __init__(self, case_sensitive=False):
        self.case_sensitive = case_sensitive

    def _normalize(self, text):
        text = str(text).strip()
        return text if self.case_sensitive else text.lower()

    def check(self, assignment, answer):
        same = self._normalize(answer) == self._normalize(assignment.correct_answer)
        return 1.0 if same else 0.0


class Student:
    """Информация о студенте"""

    _ids = itertools.count(1)

    def __init__(self, name, group):
        self.id = next(Student._ids)
        self.name = name
        self.group = group


class Assignment:
    """Задание: условие, максимальный балл, эталонный ответ и способ проверки"""

    def __init__(self, title, condition, max_score, correct_answer, checker):
        self.title = title
        self.condition = condition
        self.max_score = max_score
        self.correct_answer = correct_answer
        self.checker = checker


class Submission:
    """Решение студента"""

    def __init__(self, student, assignment, answer):
        self.student = student
        self.assignment = assignment
        self.answer = answer


class GradeResult:
    """Результат проверки одной работы"""

    def __init__(self, submission, score):
        self.submission = submission
        self.score = score
        self.elapsed = 0.0

    def to_dict(self):
        return {
            "student_id": self.submission.student.id,
            "student": self.submission.student.name,
            "assignment": self.submission.assignment.title,
            "answer": self.submission.answer,
            "score": self.score,
            "max_score": self.submission.assignment.max_score,
            "time_sec": round(self.elapsed, 6),
        }


class Grader:
    """Проверяет работы, хранит результаты, делает отчёты"""

    def __init__(self):
        self.results = []

    @timed
    def grade(self, submission):
        assignment = submission.assignment
        fraction = assignment.checker.check(assignment, submission.answer)
        score = round(fraction * assignment.max_score, 2)
        result = GradeResult(submission, score)
        self.results.append(result)
        return result

    def student_report(self, student):
        scores = [r.score for r in self.results if r.submission.student is student]
        if not scores:
            return {"student": student.name, "works": 0,
                    "average": None, "max": None, "min": None}
        return {
            "student": student.name,
            "works": len(scores),
            "average": round(sum(scores) / len(scores), 2),
            "max": max(scores),
            "min": min(scores),
        }

    def to_json(self):
        data = [r.to_dict() for r in self.results]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_json())

katya = Student("Катя", "Б25-501")
valentin = Student("Валентин", "Б25-501")

math_task = Assignment("Умножение", "Сколько будет 12 * 7?", 10, 84, NumericChecker())
sqrt_task = Assignment("Корень", "Чему равен корень из 2 (точность 0.01)?",
                       5, 1.41421, NumericChecker(tolerance=0.01))
geo_task = Assignment("География", "Столица Франции?", 5, "Париж", TextChecker())

grader = Grader()

submissions = [
    Submission(katya, math_task, "84"),
    Submission(katya, sqrt_task, "1,41"),
    Submission(katya, geo_task, "  париж "),
    Submission(valentin, math_task, "85"),
    Submission(valentin, sqrt_task, "1.5"),
    Submission(valentin, geo_task, "Париж"),
]

for sub in submissions:
    res = grader.grade(sub)
    print(f"{sub.student.name:9} | {sub.assignment.title:10} | "
          f"{res.score}/{sub.assignment.max_score} | {res.elapsed:.6f} с")

print()
for student in (katya, valentin):
    print(grader.student_report(student))

grader.save("results.json")
print()
print(grader.to_json())