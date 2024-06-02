import datetime
from typing import Optional

from correct_hours.types import ASCII_OFFSET


def parse_date(date_string: str) -> datetime.date:
    parsed_datetime = datetime.datetime.strptime(date_string, "%d/%m/%Y")
    return parsed_datetime.date()


def get_col_number(col_name: str) -> int:
    col_number_ascii = ord(col_name)
    return col_number_ascii - ASCII_OFFSET


def get_col_name(col_number: int) -> str:
    return chr(col_number + ASCII_OFFSET)


def trim_rate_label(rate_label: str) -> str:
    return str.strip(rate_label) if rate_label else ""
