import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
import math 
from util import *

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
        "detailedFilter": {"page": 1, "pageSize": 1000, "sortColumn": "DATE"}
    }

    response = requests.post(WEEKLY_REPORT_URL, headers=headers, json=data)
    response_json = response.json()
    # print_formatted_json(response_json)
    total_time = response_json["totals"][0]["totalTime"]
    time_string = seconds_to_timestring(total_time)
    time_string_hhmmss = seconds_to_timestring_hhmmss(total_time)
    # print("Total time: (HH/MM/SS) = ", time_string_hhmmss)
    time_for_each_project = {}
    time_for_each_day = {6:0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for i in range(0, len(response_json["timeentries"])):
        entry = response_json["timeentries"][i]
        duration = entry["timeInterval"]["duration"]

        # Pull the day of the week, and tally the duration for that day.
        day_of_week = (datetime.strptime(entry['timeInterval']['start'][0:10], "%Y-%m-%d")).weekday()
        time_for_each_day[day_of_week] = time_for_each_day[day_of_week] + duration

        # Pull the project name and task name, and tally the duration for that project/task
        if 'projectName' in entry.keys():
            project = entry['projectName'] 
        else:
            project = '(No Project)'
        task = entry['taskName']
        if project not in time_for_each_project.keys():
            time_for_each_project[project] = {}
        if task not in time_for_each_project[project].keys():
            time_for_each_project[project][task] = duration
        else:
            time_for_each_project[project][task] = time_for_each_project[project][task] + duration



    # Display the weekly report the following way:
    #
    # Weekly Report (Workspace Name)
    # (Date Range)
    # -------------------------
    # Total time: X 
    # 
    # Sunday: X
    # Monday: X
    # Tuesday: X
    # Wedneday: X
    # Thursday: X
    # Friday: X
    # Saturday: X
    # --------------------------
    # Project 1: X 
    #   - Task 1: X 
    #   - Task 2: X
    # --------------------------
    # Project 2: X
    # And so on....

    print(f"Weekly Report ({workspace['name']})\nSunday, {format_date(last_sunday)} -> {get_day_of_week()}, {format_date(current_date)}")
    print("--------------------------------------------------------------")
    print("Total time: ", time_string, "\n")
    for day in time_for_each_day.keys():
        print(f"{get_day_of_week(day)}: {seconds_to_timestring(time_for_each_day[day])}")
    print("--------------------------------------------------------------")
    for project in time_for_each_project:
        project_time = sum(time_for_each_project[project].values())
        print(project, ": ", seconds_to_timestring(project_time))
        for task, duration in time_for_each_project[project].items():
            print(f"    - {task}: {seconds_to_timestring_hhmmss(duration)}")
        print("--------------------------------------------------------------")

def add_time_entry(workspace):
    URL = f"https://api.clockify.me/api/v1/workspaces/{workspace['id']}/time-entries"
    headers={"x-api-key": API_KEY}
    data={
        "start": get_now_utc(),
    }
    response = requests.post(URL, headers=headers, json=data)
    print("Time entry has started.")

def is_entry_in_progress(workspace):
    URL = f"https://api.clockify.me/api/v1/workspaces/{workspace['id']}/time-entries/status/in-progress"
    headers={"x-api-key": API_KEY}
    data={
        "page": 1,
        "page-size": 1000
    }
    response = requests.get(URL, headers=headers, json=data)
    if(response.json()):
        return [response.json()[0]['id'], response.json()[0]['timeInterval']['start']]
    else:
        print("There are currently no time entries in progress")
        return False

def stop_running_time_entry(workspace):
    entry_data = is_entry_in_progress(workspace)
    if(entry_data):
        URL = f"https://api.clockify.me/api/v1/workspaces/{workspace['id']}/time-entries/{entry_data[0]}"
        headers={"x-api-key": API_KEY}
        data={
            "start": entry_data[1],
            "end": get_now_utc()
        }
        response = requests.put(URL, headers=headers, json=data)
        print("In progress time entry has been stopped")
workspaces = get_workspaces()

print("\n\n")

get_current_weekly_report(workspaces[0])
# is_entry_in_progress(workspaces[0])
# add_time_entry(workspaces[0])
# is_entry_in_progress(workspaces[0])
stop_running_time_entry(workspaces[0])

