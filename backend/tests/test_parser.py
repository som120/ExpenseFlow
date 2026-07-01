from app.parser.service import TransactionMessageParser


def test_parse_personal_expense():
    parsed = TransactionMessageParser().parse("450 coffee")

    assert parsed is not None
    assert parsed.transaction_type == "personal"
    assert str(parsed.amount) == "450"
    assert parsed.category_name == "Food"


def test_parse_income_message():
    parsed = TransactionMessageParser().parse("Received 45000 salary")

    assert parsed is not None
    assert parsed.transaction_type == "income"
    assert str(parsed.my_share) == "45000"
    assert parsed.category_name == "Salary"


def test_parse_shared_message():
    parsed = TransactionMessageParser().parse("Dinner 900 with Om Rahul")

    assert parsed is not None
    assert parsed.transaction_type == "shared"
    assert str(parsed.my_share) == "300.00"
    assert [participant.name for participant in parsed.participants] == ["Om", "Rahul"]


def test_parse_borrowed_message():
    parsed = TransactionMessageParser().parse("Cab 450 paid by Om")

    assert parsed is not None
    assert parsed.transaction_type == "borrowed"
    assert parsed.payment_owner == "Om"
    assert str(parsed.my_share) == "225.00"
