from datetime import datetime, timedelta
import math 
import json 

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

# Takes in seconds, and outputs the time in the following string format:
# H Hours, M Minutes, S Seconds
def seconds_to_timestring(seconds):
    hours = math.floor(seconds / 60 / 60)
    minutes = math.floor((seconds / 60) % 60)
    seconds = math.floor(seconds % 60)
    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(hours) + " hours, " + str(minutes) + " minutes " + str(seconds) + " seconds."

# Takes in seconds, and outputs the time in the following string format:
# HH:MM:SS
def seconds_to_timestring_hhmmss(seconds):
    hours = math.floor(seconds / 60 / 60)
    minutes = math.floor((seconds / 60) % 60)
    seconds = math.floor(seconds % 60)
    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

def print_formatted_json(response_json):
    json_formatted = json.dumps(response_json, indent=4)
    print(json_formatted)