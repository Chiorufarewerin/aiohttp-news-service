import datetime


def format_date(date: datetime.datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def parse_datetime(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(value)


def current_datetime() -> datetime.datetime:
    return datetime.datetime.utcnow()
