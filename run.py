import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
import math 
from util import get_now, get_last_sunday

load_dotenv()
API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

def print_formatted_json(response_json):
    json_formatted = json.dumps(response_json, indent=4)
    print(json_formatted)

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
            'id': response_json[i]['id'],
            'name': response_json[i]['name']
        })
    return workspaces

def get_current_weekly_report(workspace):

    current_date = get_now()
    last_sunday = get_last_sunday()

    REPORTS_API_URL="https://reports.api.clockify.me/v1/workspaces/"
    WORKSPACE_ID=workspace['id']
    WEEKLY_REPORT_URL = REPORTS_API_URL + WORKSPACE_ID + "/reports/detailed/"
    headers={"x-api-key": API_KEY}
    data={
        "dateRangeEnd": current_date, 
        "dateRangeStart": last_sunday,
        "detailedFilter": {"page": 1, "pageSize": 1000} 
    }

    print(current_date)
    print(last_sunday)
    print(WEEKLY_REPORT_URL)

    response = requests.post("https://reports.api.clockify.me/v1/workspaces/" + WORKSPACE_ID + "/reports/detailed", headers=headers, json=data)
    response_json = response.json()
    print_formatted_json(response_json)
    total_time = response_json["totals"][0]["totalTime"]
    hours = math.floor(total_time / 60 / 60)
    minutes = math.floor((total_time / 60) % 60)
    seconds = math.floor(total_time % 60)
    time_string = str(hours) + " hours, " + str(minutes) + " minutes " + str(seconds) + " seconds."
    print("Total time: ", time_string)
    for i in range(0, len(response_json["timeentries"])):
        entry = response_json["timeentries"][i]
        duration = entry["timeInterval"]["duration"]
        project = entry['projectName']
        task = entry['taskName']
        print("Entry ", i, ") ", duration, "| ", project, " | ", task, " |")

workspaces = get_workspaces()
print(workspaces)

get_current_weekly_report(workspaces[0])