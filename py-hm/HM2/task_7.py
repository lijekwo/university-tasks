import pathlib

directory = input()
extensions = input()

a = pathlib.Path(directory)

if not a.exists() or not a.is_dir():
    print("Error")
else:
    for i  in a.rglob(f"*{extensions}"):
        if i.is_file():
            print(str(i))
            print(i.stat().st_size)
