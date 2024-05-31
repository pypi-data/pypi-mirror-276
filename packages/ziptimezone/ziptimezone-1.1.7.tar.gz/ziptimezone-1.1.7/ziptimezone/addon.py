from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
import pytz
from .core import get_lat_long_for_zip, get_timezone_without_map_by_zip


def get_sunrise_sunset(zip_code, date=None):
    """
    Calculate sunrise and sunset times for a given ZIP code on a specified date, considering DST adjustments.
    If no date is provided, today's date is used.

    Parameters:
        zip_code (str): The ZIP code for which to calculate sunrise and sunset times.
        date (datetime.date, optional): The date for which to calculate the times. Defaults to today's date if not provided.

    Returns:
        dict: A dictionary containing the sunrise and sunset times as strings (local time),
              with keys 'sunrise_time' and 'sunset_time'.
    """

    latitude, longitude = get_lat_long_for_zip(zip_code)

    timezone_str = get_timezone_without_map_by_zip(zip_code)
    timezone = pytz.timezone(timezone_str)

    # Determine the date to use, default to today if none provided
    if date is None:
        date = datetime.now(timezone).date()

    # Create a LocationInfo object with the correct timezone
    location = LocationInfo(
        latitude=latitude, longitude=longitude, timezone=timezone_str
    )

    # Localize the specified or default date to the specified timezone
    local_date = datetime.combine(date, datetime.min.time())  # No time component
    local_date = timezone.localize(
        local_date
    )  # Localize the date to the specified timezone

    # Calculate sunrise and sunset times using the localized date
    s = sun(location.observer, date=local_date, tzinfo=timezone)

    # Extract and format sunrise and sunset times
    sunrise_time = s["sunrise"].strftime("%H:%M:%S")
    sunset_time = s["sunset"].strftime("%H:%M:%S")

    return {"sunrise_time": sunrise_time, "sunset_time": sunset_time}
