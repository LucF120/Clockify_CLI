import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

def print_formatted_json(response_json):
    json_formatted = json.dumps(response_json, indent=4)
    print(json_formatted)

def get_last_sunday():
    # Get the current datetime
    now = datetime.now()

    # Calculate days to subtract to get to the previous Sunday
    days_since_sunday = now.weekday() + 1  # .weekday() gives Monday as 0, Sunday as 6

    # Subtract those days and reset the time to 12:00 AM
    previous_sunday = now - timedelta(days=days_since_sunday)
    previous_sunday_midnight = previous_sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Format the output
    return previous_sunday_midnight.isoformat() + '.000000Z'

def get_workspaces():
    URL = "https://api.clockify.me/api/v1/workspaces"
    headers={"x-api-key": API_KEY}
    response = requests.get(URL, headers=headers)
    response_json = response.json()
    print_formatted_json(response_json)

    # Return all workspace ids as an array of dicts  
    workspaces = []    
    for i in range(0, len(response_json)):
        workspaces.append({
            response_json[i]['id']: response_json[i]['name']
        })
    return workspaces

get_workspaces()

# current_date = datetime.now().isoformat(timespec='microseconds') + 'Z'
# last_sunday = get_last_sunday()

# REPORTS_API_URL="https://reports.api.clockify.me/v1/workspaces/"
# WORKSPACE_ID=""
# WEEKLY_REPORT_URL = REPORTS_API_URL + WORKSPACE_ID + "/reports/weekly"
# headers={"x-api-key": API_KEY}
# data={"dateRangeStart": last_sunday, "dateRangeEnd": current_date, "exportType": "JSON"}

# print(current_date)
# print(last_sunday)
# print(WEEKLY_REPORT_URL)

# response = requests.post(WEEKLY_REPORT_URL, headers=headers, json=data)
# print(response.json())