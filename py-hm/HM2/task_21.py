import re

def is_valid_login(login):
    return re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{3,15}", login) is not None

tests = ["user_123", "admin", "123user", "ab", "user-name", "very_long_username"]

for login in tests:
    print(f"{login:20} → {is_valid_login(login)}")