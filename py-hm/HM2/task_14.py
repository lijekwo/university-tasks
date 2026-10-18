from contextlib import contextmanager

@contextmanager
def log_operation(filename, name):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"START: {name}\n")
        try:
            yield
        except BaseException:
            f.write(f"ERROR: {name}\n")
            raise
        else:
            f.write(f"END: {name}\n")