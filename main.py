import random
import datetime
import csv
from csv import DictWriter, DictReader

n, seed = input().split()

merchants = {
    "Пятёрочка": "Продукты",
    "Магнит": "Продукты",
    "Яндекс Go": "Транспорт",
    "Метро": "Транспорт",
    "Кофейня": "Кафе",
    "Ozon": "Покупки",
    "Wildberries": "Покупки",
    "Кинотеатр": "Развлечения",
    "Вкусно и точка": "Рестораны"
}

def generate_date(rng, min_date = datetime.date(2000, 1, 1),
                  max_date = datetime.datetime.now().date()):
    delta = max_date - min_date
    rdays = rng.randint(0, delta.days)
    return min_date + datetime.timedelta(days=rdays)

def generate_transactions(n, seed):
    r = random.Random(seed)
    transactions = []
    for x in range(n):
        i = {"date": f"{generate_date(r)}", "merchant": f"{r.choice(list(merchants.keys()))}",
             "amount": r.randint(1, 999999), "category": ""}
        i["category"] = merchants[i["merchant"]]
        transactions.append(i)
    return transactions

with open("transactions.csv", 'w', encoding='utf-8', newline='') as csvfile:
    writer = DictWriter(csvfile, fieldnames=["date", "merchant", "amount", "category"])
    writer.writeheader()
    writer.writerows(generate_transactions(int(n), seed))

with open('transactions.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        print(row)



