from datetime import datetime


def utc_now() -> datetime:
    return datetime.now(tz=datetime.UTC)
