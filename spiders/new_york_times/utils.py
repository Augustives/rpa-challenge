from datetime import datetime, timedelta
from dataclasses import dataclass


def get_date_range(months_ago: int) -> tuple[datetime, datetime]:
    months_ago = max(1, int(months_ago))

    today = datetime.now().date()

    if months_ago == 1:
        date_since = today.replace(day=1)
    else:
        days_to_subtract = (months_ago - 1) * 30 + 1
        date_since = (today.replace(day=1) - timedelta(days=days_to_subtract)).replace(
            day=1
        )

    return today, date_since


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b. %d, %Y").date()
    except ValueError:
        current_year = datetime.now().year
        return datetime.strptime(f"{date_str}, {current_year}", "%b. %d, %Y").date()
