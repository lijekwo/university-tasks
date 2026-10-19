import re

text = """Полезные сайты: https://python.org, http://example.com/page,
https://example.com/docs/index.html и ftp://files.example.com/data."""

urls = re.findall(r"https?://[^\s,]+[^\s,.]", text)

for url in urls:
    print(url)