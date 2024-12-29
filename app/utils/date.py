from datetime import date, datetime
from typing import Union

import arrow
from arrow import Arrow

DEFAULT_FORMAT = "YYYY-MM-DD HH:mm:ss"
SIMPLE_FORMAT = "YYYY-MM-DD"
SHORT_DATE_FORMAT = "YYYYMMDD"


def get_now_millis():
    return arrow.now().int_timestamp * 1000


def get_now() -> Arrow:
    return arrow.now()


def get_today() -> date:
    return arrow.now().date()


def date_format(
    value: Union[Arrow | datetime | date], format_str: str = DEFAULT_FORMAT
) -> str:
    if isinstance(value, Arrow):
        return value.format(format_str)
    return arrow.get(value).format(format_str)


def now_format(format_str: str = DEFAULT_FORMAT):
    return date_format(get_now(), format_str)


def date_parse(value: Union[str | datetime, date]) -> Arrow:
    return arrow.get(value)


def date_parse_to_date(value: Union[str | datetime, date]) -> date:
    return date_parse(value).date()
