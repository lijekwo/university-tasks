import re

products = [
    "PRD-12345",
    "PRD-00123",
    "USR-12345",
    "PRD-987",
    "PRD-ABCDE",
    "PRD-54321"
]

valid = [p for p in products if re.fullmatch(r"PRD-\d{5}", p)]

print(valid)