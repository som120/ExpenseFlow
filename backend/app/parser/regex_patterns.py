import re


AMOUNT_PATTERN = re.compile(r"(?P<amount>[+-]?\d+(?:\.\d{1,2})?)")
WITH_PATTERN = re.compile(r"\bwith\s+(?P<participants>[A-Za-z][A-Za-z\s]+)$", re.IGNORECASE)
PAID_BY_PATTERN = re.compile(r"\bpaid\s+by\s+(?P<payer>[A-Za-z][A-Za-z\s]+)$", re.IGNORECASE)
RECEIVED_PATTERN = re.compile(r"^(received|got|income|\+)\b", re.IGNORECASE)
SPENT_PATTERN = re.compile(r"^(spent|paid|-)?\s*", re.IGNORECASE)
