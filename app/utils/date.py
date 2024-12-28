import arrow
from arrow import Arrow

DEFAULT_FORMAT = "YYYY-MM-DD HH:mm:ss"
SIMPLE_FORMAT = "YYYY-MM-DD"
SHORT_DATE_FORMAT = "YYYYMMDD"


def get_now_millis():
    return arrow.now().int_timestamp * 1000


def get_now() -> Arrow:
    return arrow.now()


def date_format(date: Arrow, format_str: str = DEFAULT_FORMAT):
    return date.format(format_str)


def now_format(format_str: str = DEFAULT_FORMAT):
    return date_format(get_now(), format_str)


def date_parse(date_str: str) -> Arrow:
    return arrow.get(date_str)
