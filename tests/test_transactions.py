from collections import Counter

from main import generate_transactions, write_transactions, load_transactions, categorize

def test_generate_transactions():
    first = generate_transactions(10, 1)
    second = generate_transactions(10, 1)

    assert first == second
    assert len(first) == 10


def test_full_cycle_csv(tmp_path):
    file_path = tmp_path/"tmp_csv.csv"
    original = generate_transactions(5, 1)
    write_transactions(original, file_path)
    loaded, errors = (load_transactions(file_path)[0], load_transactions(file_path)[1])
    assert original == loaded
    assert not errors


def test_csv(tmp_path):
    new_path = tmp_path / "csvfile.csv"
    old_csv = [{"date": "2026-11-23", "merchant": "Пятёрочка", "amount": 1, "category": "t"},
               {"date": "2026-11-", "merchant": "Покупка WB", "amount": 1, "category": "t"},
               {"date": "2026-11-23", "merchant": "Неизвестный магазин", "amount": 1, "category": ""},
               {"date": "2026-11-23", "merchant": "Ozon", "amount": "abc", "category": ""}]
    write_transactions(old_csv, new_path)
    loaded, errors = (load_transactions(new_path)[0],
                      load_transactions(new_path)[1])
    assert len(loaded) == 1
    assert len(errors) == 3


def test_categorize():
    assert categorize({"date": "2026-11-23", "merchant": "пятёрочка", "amount": 1, "category": ""},
                      "kw") == "Продукты"
    assert categorize({"date": "2026-11-23", "merchant": "Покупка WB", "amount": 1, "category": ""},
                      "kw") == "Покупки"
    assert categorize({"date": "2026-11-23", "merchant": "Неизвестный магазин", "amount": 1, "category": ""},
                      "kw") == "Прочее"
    assert categorize({"date": "2026-11-23", "merchant": "Покупка WB", "amount": 1, "category": ""},
                      "fm") == "Прочее"
    assert categorize({"date": "2026-11-23", "merchant": "Кино Мак", "amount": 1, "category": ""},
                      "kw") == "Развлечения"


def test_coverage(tmp_path):
    new_path = tmp_path/"csvfile.csv"
    old_csv = [{"date": "2026-11-23", "merchant": "Пятёрочка", "amount": 1, "category": "t"},
               {"date": "2026-11-23", "merchant": "Покупка WB", "amount": 1, "category": "t"},
               {"date": "2026-11-23", "merchant": "Неизвестный магазин", "amount": 1, "category": "t"},
               {"date": "2026-11-23", "merchant": "Ozon", "amount": "abc", "category": ""}]
    write_transactions(old_csv, new_path)
    transactions, errors, coverage, categorized, top_10 = load_transactions(new_path)
    assert len(transactions) == 3
    assert len(errors) == 1
    assert categorized == 2
    assert len(transactions) - categorized == 1
    assert coverage == 66.67
    assert transactions[0]["category"] == "Продукты"
    assert transactions[1]["category"] == "Покупки"
    assert transactions[2]["category"] == "Прочее"


def test_empty_csv(tmp_path):
    new_path = tmp_path/"csv_file.csv"
    old_csv = []
    write_transactions(old_csv, new_path)
    transactions, errors, coverage, categorized, top_10 = load_transactions(new_path)
    assert len(transactions) == 0
    assert len(errors) == 0
    assert coverage == 0

def test_top_merchants():
    transactions, errors, coverage, categorized, top_10 = load_transactions("tests/test_transactions.csv")
    expected_top_10 = [
        ("Мерчант Альфа", 4),
        ("Мерчант Бета", 2),
        ("Мерчант Гамма", 1),
        ("Мерчант Дельта", 1),
        ("Мерчант Эпсилон", 1),
        ("Мерчант Дзета", 1),
        ("Мерчант Эта", 1),
        ("Мерчант Тета", 1),
        ("Мерчант Йота", 1),
        ("Мерчант Каппа", 1)
    ]
    assert expected_top_10 == top_10
    assert "Ozon" not in [i[0] for i in top_10]