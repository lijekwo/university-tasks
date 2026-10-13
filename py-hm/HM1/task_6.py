import random
from collections import Counter
from datetime import datetime

METHODS = ["GET", "POST", "PUT", "DELETE"]
URLS = ["/index.html", "/login", "/logout", "/about", "/contact", "/products", "/cart", "/api/users", "/api/orders", "/search"]
STATUSES = [200, 201, 301, 304, 400, 403, 404, 500, 502]

def random_ip():
    return '.'.join(str(random.randint(0, 255)) for i in range(4))

def make_good_line(ip_pool):
    date = f'2026-09-{random.randint(1,30):02d}'
    clock = f'{random.randint(0,23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}'
    ip = random.choice(ip_pool)
    method = random.choice(METHODS)
    url = random.choice(URLS)
    status = random.choice(STATUSES)
    return f'{date} {clock} {ip} {method} {url} {status}'

def make_bad_line():
    kind = random.randint(1, 7)
    if kind == 1:
        return ""
    if kind == 2:
        return "это просто мусор в логе"
    if kind == 3:
        return "2026-09-01 12:15:31 192.168.1.10 GET /index.html"
    if kind == 4:
        return "2026-09-01 12:15:31 999.1.1.1 GET /login 200"
    if kind == 5:
        return "2026-09-01 12:15:31 192.168.1.10 GET /login abc"
    if kind == 6:
        return "2026-09-01 12:15:31 192.168.1.10 FETCH /login 200"
    return "2026-13-45 12:15:31 192.168.1.10 GET /login 200"

def generate_log(filename, n = 10_000, bad_share = 0.05):
    ip_pool = [random_ip() for i in range(300)]

    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(n):
            if random.random() < bad_share:
                line = make_bad_line()
            else:
                line = make_good_line(ip_pool)
            f.write(line + '\n')

def parse_line(line):
    parts = line.split()
    if len(parts) != 6:
        return None

    date, clock, ip, method, url, status = parts

    try:
        datetime.strptime(date + ' ' + clock, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

    octets = ip.split('.')
    if len(octets) != 4:
        return None
    for o in octets:
        if not o.isdigit() or int(o) > 255:
            return None

    if method not in METHODS:
        return None
    if not url.startswith('/'):
        return None
    if not status.isdigit() or not 100 <= int(status) <= 599:
        return None

    return ip, method, url, int(status)

def analyze_log(filename):
    total = 0
    bad = 0
    errors_4xx = 0
    ips = Counter()
    methods = Counter()
    urls = Counter()

    with open(filename, encoding='utf-8') as f:
        for line in f:
            result = parse_line(line)
            if result is None:
                bad += 1
                continue

            ip, method, url, status = result
            total += 1
            ips[ip] += 1
            methods[method] += 1
            urls[url] += 1
            if 400 <= status <= 499:
                errors_4xx += 1

    return {
        'total': total,
        'bad': bad,
        'unique_ips': len(ips),
        'top_ip': ips.most_common(1)[0],
        'methods': methods,
        'errors_4xx': errors_4xx,
        'top_url': urls.most_common(1)[0],
    }

generate_log('server.log')
r = analyze_log('server.log')

print("Корректных запросов:", r["total"])
print("Некорректных строк пропущено:", r["bad"])
print("Уникальных IP:", r["unique_ips"])
print("Самый активный IP: {} ({} запросов)".format(*r["top_ip"]))
print("Запросы по методам:")
for method, count in r["methods"].items():
    print(f"  {method}: {count}")
print("Ошибок 4xx:", r["errors_4xx"])
print("Самый частый URL: {} ({} раз)".format(*r["top_url"]))