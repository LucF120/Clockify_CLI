import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
import math 
from util import seconds_to_timestring, seconds_to_timestring_hhmmss, get_now, get_last_sunday, print_formatted_json, get_day_of_week, format_date

load_dotenv()
API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

def get_workspaces():
    URL = "https://api.clockify.me/api/v1/workspaces"
    headers={"x-api-key": API_KEY}
    response = requests.get(URL, headers=headers)
    response_json = response.json()
    # print_formatted_json(response_json)

    # Return all workspace ids as an array of dicts  
    workspaces = []    
    print("Workspaces:")
    print("--------------------------------------------------------------")
    for i in range(0, len(response_json)):
        name = response_json[i]['name']
        print(i+1, ": ", response_json[i]['name'])
        workspaces.append({
            'id': response_json[i]['id'],
            'name': name
        })
    print("--------------------------------------------------------------")
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

    response = requests.post("https://reports.api.clockify.me/v1/workspaces/" + WORKSPACE_ID + "/reports/detailed", headers=headers, json=data)
    response_json = response.json()
    # print_formatted_json(response_json)
    total_time = response_json["totals"][0]["totalTime"]
    time_string = seconds_to_timestring(total_time)
    time_string_hhmmss = seconds_to_timestring_hhmmss(total_time)
    print(f"Weekly Report: (Sunday, {format_date(last_sunday)} -> {get_day_of_week()}, {format_date(current_date)})")
    print("--------------------------------------------------------------")
    print("Total time: ", time_string)
    # print("Total time: (HH/MM/SS) = ", time_string_hhmmss)
    time_for_each_project = {}
    for i in range(0, len(response_json["timeentries"])):
        entry = response_json["timeentries"][i]
        duration = entry["timeInterval"]["duration"]
        project = entry['projectName']
        task = entry['taskName']
        
        if project not in time_for_each_project.keys():
            time_for_each_project[project] = {}
        if task not in time_for_each_project[project].keys():
            time_for_each_project[project][task] = duration
        else:
            time_for_each_project[project][task] = time_for_each_project[project][task] + duration

    print("--------------------------------------------------------------")
    for project in time_for_each_project:
        project_time = sum(time_for_each_project[project].values())
        print(project, ": ", seconds_to_timestring(project_time))
        for task, duration in time_for_each_project[project].items():
            print("         ", task, ":", seconds_to_timestring_hhmmss(duration))
        print("--------------------------------------------------------------")


workspaces = get_workspaces()

print("\n\n")

get_current_weekly_report(workspaces[0])