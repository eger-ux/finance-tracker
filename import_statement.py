from csv import DictReader
from main import categorize, write_transactions
import datetime, re


def import_statement(input_path, output_path):
    with open(input_path, 'r', encoding="utf-8", newline='') as csvfile:
        reader = DictReader(csvfile)
        errors = []
        transactions = []
        n = 0
        date_count = merchant_count = amount_count = 0
        if not reader.fieldnames:
            print("CSV пустой или отсутствуют заголовки.")
            return 0
        for i in reader.fieldnames:
            if i in ["Date", "date", "Дата", "Дата операции"]:
                date_count += 1
                date_name = i
            elif i in ["merchant", "Продавец", "Описание"]:
                merchant_count += 1
                merchant_name = i
            elif i in ["amount", "Сумма"]:
                amount_count += 1
                amount_name = i
        if date_count == merchant_count == amount_count == 1:
            for row in reader:
                n += 1
                date = row[date_name]
                merchant = row[merchant_name]
                amount = row[amount_name]
                if date is None or merchant is None or amount is None or date.strip() == (""
                    "") or merchant.strip() == "" or amount.strip() == "":
                    errors.append(f'Пустое поле в строке {n}')
                    continue
                try:
                    if '-' in date:
                        d = date.split('-')
                        if not (len(d) == 3 and len(d[0]) == 4 and len(d[1]) == len(d[2]) == 2):
                            raise ValueError
                        d = list(map(int, d))
                        date = datetime.date(d[0], d[1], d[2])
                    elif '.' in date:
                        d = date.split('.')
                        if not (len(d) == 3 and len(d[2]) == 4 and len(d[1]) == len(d[0]) == 2):
                            raise ValueError
                        d = list(map(int, d))
                        date = datetime.date(d[2], d[1], d[0])
                    else:
                        raise ValueError
                except ValueError:
                    errors.append(f"Неверный формат даты в строке {n}")
                    continue

                if re.fullmatch(r'([1-9][0-9]{1,2}( [0-9]{3})*(\.0+)?)|([1-9][0-9]*(\.0+)?)', amount):
                    amount = int(((''.join(amount.split())).split('.'))[0])
                else:
                    errors.append(f"Неверный формат суммы в строке {n}")
                    continue

                transactions.append({"date": date, "merchant": merchant, "amount": amount})

            for i in transactions:
                category = categorize(i, 'kw')
                i["category"] = category

            write_transactions(transactions, output_path)
            print("Импорт завершен.")
            print(f"Импортировано строк: {len(transactions)}")
            print("Ошибки:", errors)
            return transactions, len(transactions), errors

        else:
            print("Ошибка названий столбцов/пустой файл. Импорт не завершен.")
            return 0


input_path = input("Введите путь к файлу: ")

import_statement(input_path, "transactions.csv")