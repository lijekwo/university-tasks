import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.perf_counter() - self.start
        print(f"Время выполнения: {elapsed:.4f} сек")
        return False

def some_function():
    time.sleep(0.5)

with Timer():
    some_function()