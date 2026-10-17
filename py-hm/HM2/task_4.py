from csv import DictReader, DictWriter
with open("expensive.csv") as f:
    with open("new_expensive.csv", "w", newline='') as d:
        reader = DictReader(f)
        writer = DictWriter(d, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if int(row["price"]) > 100:
                writer.writerow(row)