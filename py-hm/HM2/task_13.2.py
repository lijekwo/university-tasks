import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Время выполнения: {elapsed:.4f} сек")

def some_function():
    time.sleep(0.5)

with timer():
    some_function()