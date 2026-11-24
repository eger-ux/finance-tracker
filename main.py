import random
import datetime
from csv import DictWriter, DictReader
from collections import Counter

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

key_words_of_merchants = {
    "Go": "Яндекс Go",
    "Кофейня": "Кофейня",
    "WB": "Wildberries",
    "Кино": "Кинотеатр",
    "Мак": "Вкусно и точка"
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


def write_transactions(file_path, new_path):
    with open(new_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=["date", "merchant", "amount", "category"])
        writer.writeheader()
        writer.writerows(file_path)


def load_transactions(path):
    with open(path, 'r', encoding='utf-8', newline='') as file:
        reader = DictReader(file)
        n = 0
        categorized = 0
        uncategorized_merchants = []
        transactions = []
        errors = []
        for row in reader:
            n += 1
            if len([1 for i in row if row[i]]) != 4:
                errors.append(f"Ошибка в строке {n}: пустое поле.")
                continue
            if list(row.keys()) != ["date", "merchant", "amount", "category"]:
                errors.append(f"Ошибка в строке {n}: некорректная структура CSV.")
                continue

            try:
                d = row['date'].split('-')
                if not(len(d) == 3 and len(d[0]) == 4 and len(d[1]) == len(d[2]) == 2):
                    raise ValueError
                d = list(map(int, d))
                datetime.date(d[0], d[1], d[2])
            except ValueError:
                errors.append(f"Ошибка в строке {n}: некорректная дата.")
                continue

            try:
                row["amount"] = int(row["amount"])
            except ValueError:
                errors.append(f"Ошибка в строке {n}: сумма не является числом.")
                continue
            else:
                if row["amount"] <= 0:
                    errors.append(f"Ошибка в строке {n}: сумма не положительна.")
                    continue

            category = categorize(row, 'kw')
            if category != "Прочее":
                categorized += 1
            else:
                uncategorized_merchants.append(row["merchant"])
            row['category'] = category

            transactions.append(row)

        top_10 = Counter(uncategorized_merchants).most_common(10)
        try:
            coverage = round(categorized / len(transactions) * 100, 2)
        except ZeroDivisionError:
            coverage = 0


        return transactions, errors, coverage, categorized, top_10


def categorize(tx, rules):
    category = "Прочее"
    if rules == "fm":
        if tx["merchant"] in merchants.keys():
            category = merchants[tx["merchant"]]
    elif rules == 'kw':
        for name, value in merchants.items():
            if name.casefold() == tx["merchant"].casefold():
                category = value
                break
        else:
            for i in key_words_of_merchants.keys():
                if i.casefold() in tx["merchant"].casefold():
                    category = merchants[key_words_of_merchants[i]]
                    break
    return category


if __name__ == "__main__":
    n, seed = map(int, input().split())
    write_transactions(generate_transactions(n, seed), "transactions.csv")
    print(load_transactions("tests/test_transactions.csv"))