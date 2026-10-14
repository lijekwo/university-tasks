import functools
import inspect


def validate_types(*types):

    def decorator(func):
        sig = inspect.signature(func)

        required = [
            name for name, param in sig.parameters.items()
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
            and param.default is param.empty
        ]

        if len(types) != len(required):
            raise TypeError(
                f"Функция '{func.__name__}' имеет {len(required)} обязательных "
                f"позиционных аргумент(ов), а передано типов: {len(types)}"
            )

        expected = dict(zip(required, types))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)

            for name, expected_type in expected.items():
                value = bound.arguments[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Аргумент '{name}' функции '{func.__name__}' должен "
                        f"быть типа {expected_type.__name__}, "
                        f"а получен {type(value).__name__}: {value!r}"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator

@validate_types(int, int)
def add(a, b):
    """Складывает два числа"""
    return a + b


@validate_types(str, int)
def greet(name, age, greeting="Привет"):
    """Приветствие"""
    return f"{greeting}, {name}! Тебе {age}."


@validate_types(int)
def total(first, *others):
    """Сумма любого количества чисел"""
    return first + sum(others)

print(add(2, 3))
print(add(a=10, b=20))
try:
    add(2, "3")
except TypeError as e:
    print("Ошибка:", e)

print(greet("Аня", 18))
print(greet(age=19, name="Иван", greeting="Здравствуй"))
try:
    greet("Аня", "восемнадцать")
except TypeError as e:
    print("Ошибка:", e)

print(total(1))
print(total(1, 2, 3, 4))
try:
    total("1", 2, 3)
except TypeError as e:
    print("Ошибка:", e)

print(add.__name__)
print(add.__doc__)