import itertools
import json

CREATE_USER = 'create_user'
DELETE_USER = 'delete_user'
CREATE_ASSIGNMENT = 'create_assignment'
SOLVE_ASSIGNMENT = 'solve_assignment'

class PermissionDenied(Exception):
    """Ошибка: у пользователя нет прав на это действие"""

class Assignment:
    """Учебное задание"""

    _ids = itertools.count(1)

    def __init__(self, title, text, author_id):
        self.id = next(Assignment._ids)
        self.title = title
        self.text = text
        self.author_id = author_id

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'author_id': self.author_id,
        }

class User:
    """Базовый класс пользователя"""

    role = 'user'
    permissions = frozenset()
    _ids = itertools.count(1)

    def __init__(self, name):
        self.id = next(User._ids)
        self.name = name

    def can(self, permission):
        return permission in self.permissions

    def require(self, permission):
        if not self.can(permission):
            raise PermissionDenied(f"{self.role} '{self.name}' не имеет права '{permission}'")

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role}

    def __str__(self):
        return f'{self.role}: {self.name} (id = {self.id})'

class Admin(User):
    role = 'admin'
    permissions = frozenset({CREATE_USER, DELETE_USER})

class Teacher(User):
    role = 'teacher'
    permissions = frozenset({CREATE_ASSIGNMENT})

    def __init__(self, name):
        super().__init__(name)
        self.assignments = []

    def create_assignment(self, title, text):
        self.require(CREATE_ASSIGNMENT)
        assignment = Assignment(title, text, self.id)
        self.assignments.append(assignment)
        return assignment

    def to_dict(self):
        data = super().to_dict()
        data['created_assignments'] = [a.id for a in self.assignments]
        return data

class Student(User):
    role = 'student'
    permissions = frozenset({SOLVE_ASSIGNMENT})

    def __init__(self, name):
        super().__init__(name)
        self.solutions = {}

    def solve(self, assignment, answer):
        self.require(SOLVE_ASSIGNMENT)
        self.solutions[assignment.id] = answer
        return f"{self.name} решил(а) задание '{assignment.title}'"

    def to_dict(self):
        data = super().to_dict()
        data['solved_assignments'] = list(self.solutions)
        return data

class Application:
    """Управляет пользователями"""

    def __init__(self, admin_name = 'root'):
        self.users = {}
        self.root = Admin(admin_name)
        self.users[self.root.id] = self.root

    def create_user(self, actor, user_class, name):
        actor.require(CREATE_USER)
        if not issubclass(user_class, User):
            raise TypeError('user_class должен быть наследником User')
        user = user_class(name)
        self.users[user.id] = user
        return user

    def delete_user(self, actor, user_id):
        actor.require(DELETE_USER)
        if user_id == actor.id:
            raise ValueError('Нельзя удалить самого себя')
        if user_id not in self.users:
            raise ValueError(f'Пользователь с id={user_id} не найден')
        return self.users.pop(user_id)
    
    def to_json(self):
        data = [user.to_dict() for user in self.users.values()]
        return json.dumps(data, ensure_ascii=False, indent = 2)

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_json())

app = Application()
root = app.root

katya = app.create_user(root, Student, "Катя")
murat = app.create_user(root, Teacher, "Мурат Муратович")
valentin = app.create_user(root, Student, "Валентин")

print("Создали:", katya, ",", murat, ",", valentin)

task = murat.create_assignment("Задача 1", "Посчитай 2 + 2")
print(katya.solve(task, "4"))

print("Катя может создавать задания?", katya.can(CREATE_ASSIGNMENT))
print("Мурат Муратович может создавать задания?", murat.can(CREATE_ASSIGNMENT))

try:
    app.create_user(katya, Student, "Хакер")
except PermissionDenied as e:
    print("Ошибка:", e)

try:
    app.delete_user(murat, valentin.id)
except PermissionDenied as e:
    print("Ошибка:", e)

try:
    app.delete_user(root, root.id)
except ValueError as e:
    print("Ошибка:", e)

app.delete_user(root, valentin.id)

print(app.to_json())