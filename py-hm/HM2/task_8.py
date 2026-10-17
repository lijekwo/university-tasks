def read_file(path):
    try:
        with open(path, "r", encoding= "utf-8") as f:
            return f.read()
        
    except FileNotFoundError:
        print("Ошибка отсутствия файла")

    except PermissionError as e:
        print(f"Ошибка прав доступа {e}")
        
    except Exception as e:
        print(f"Error {e.__class__.__name__}")
read_file(input())