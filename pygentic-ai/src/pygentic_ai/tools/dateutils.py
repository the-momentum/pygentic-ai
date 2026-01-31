"""Date utility tools for agents."""

from datetime import datetime


def get_today_date() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_week() -> str:
    """Get the current week number and year."""
    now = datetime.now()
    return f"Week {now.isocalendar()[1]}, {now.year}"


def get_weekday_from_date(date_str: str) -> str:
    """Get the day of the week from a date string.

    Args:
        date_str: Date in YYYY-MM-DD format

    Returns:
        Day of the week (e.g., 'Monday')
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%A")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD"


DATEUTILS_TOOLS = [
    get_today_date,
    get_current_week,
    get_weekday_from_date,
]
