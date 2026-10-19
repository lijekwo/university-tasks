import json
import logging
import re
from collections import Counter
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) "
    r"(?P<method>[A-Z]+) "
    r"(?P<url>\S+) "
    r"(?P<status>\d{3})$"
)

def analyze(path):
    methods = Counter()
    urls = Counter()
    total = 0
    errors_4xx = 0
    bad_lines = 0

    with open(path, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            match = LINE_RE.match(line)
            if not match:
                bad_lines += 1
                logger.warning("Строка %d не соответствует формату: %s", number, line)
                continue

            total += 1
            methods[match["method"]] += 1
            urls[match["url"]] += 1

            if match["status"].startswith("4"):
                errors_4xx += 1

            if total % 100000 == 0:
                logger.info("Обработано запросов: %d", total)

    most_url, most_count = urls.most_common(1)[0] if urls else (None, 0)

    return {
        "total_requests": total,
        "requests_by_method": dict(methods),
        "errors_4xx": errors_4xx,
        "most_frequent_url": {"url": most_url, "count": most_count},
        "skipped_lines": bad_lines,
    }

def main():
    base = Path(__file__).parent
    source = base / "access.log"
    target = base / "stats.json"

    logger.info("Начало обработки файла %s", source)

    try:
        stats = analyze(source)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", source)
        return
    except PermissionError:
        logger.error("Нет прав доступа к файлу: %s", source)
        return
    except UnicodeDecodeError:
        logger.error("Не удалось прочитать файл (ожидается UTF-8): %s", source)
        return
    except OSError as e:
        logger.error("Ошибка операционной системы: %s", e)
        return

    try:
        with open(target, "w", encoding="utf-8") as file:
            json.dump(stats, file, indent=4, ensure_ascii=False)
    except OSError as e:
        logger.error("Не удалось записать %s: %s", target, e)
        return

    logger.info("Обработка завершена, результат сохранён в %s", target)

if __name__ == "__main__":
    main()