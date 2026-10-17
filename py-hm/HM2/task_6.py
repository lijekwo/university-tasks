from pathlib import Path

path = Path(input("Введите путь к каталогу: "))

files_count = 0
dirs_count = 0
total_size = 0
py_files = []

for item in path.rglob("*"):
    if item.is_file():
        files_count += 1
        total_size += item.stat().st_size

        if item.suffix == ".py":
            py_files.append(item)
    elif item.is_dir():
        dirs_count += 1

print("Количество файлов:", files_count)
print("Количество подкаталогов:", dirs_count)
print("Суммарный размер файлов:", total_size, "байт")

print("Список .py файлов:")
for file in py_files:
    print(" ", file)