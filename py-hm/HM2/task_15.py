from io import StringIO

def count_lines(stream):
    count = 0
    for i in stream:
        count += 1
    return count

with open("data.txt", encoding="utf-8") as f:
    print(count_lines(f))

print(count_lines(StringIO("first\nsecond\nthird")))