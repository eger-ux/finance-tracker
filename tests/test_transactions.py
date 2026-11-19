from main import generate_transactions, write_transactions, load_transactions

def test_generate_transactions():
    first = generate_transactions(10, 1)
    second = generate_transactions(10, 1)

    assert first == second
    assert len(first) == 10


def test_full_cycle_csv(tmp_path):
    file_path = tmp_path/"tmp_csv.csv"
    original = generate_transactions(5, 1)
    write_transactions(original, file_path)
    loaded, errors = load_transactions(file_path)
    assert original == loaded
    assert not errors


def test_csv():
    loaded, errors = load_transactions(r"tests\test_transactions.csv")
    assert len(loaded) == 1
    assert len(errors) == 3

