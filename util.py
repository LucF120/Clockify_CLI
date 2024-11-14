from datetime import datetime, timedelta

def get_last_sunday():
    # Get the current datetime
    now = datetime.now()

    # Calculate days to subtract to get to the previous Sunday
    days_since_sunday = now.weekday() + 1  # .weekday() gives Monday as 0, Sunday as 6

    # Subtract those days and reset the time to 12:00 AM
    previous_sunday = now - timedelta(days=days_since_sunday)
    previous_sunday_midnight = previous_sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Format the output
    return previous_sunday_midnight.isoformat()

def get_now():
    return datetime.now().isoformat()