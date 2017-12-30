'''
Fetches data from PI using REST APIs and loads into sqlite DB
'''
import requests
import ConfigParser
import sqlite3

# read properties
config = ConfigParser.RawConfigParser()
config.read('pi.properties')
base_url = config.get('api', 'base.url')
api_token = config.get('api', 'api.token')

headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'api-token': api_token}

# projects
url = base_url + "/api/project/active"
model_props = ["id", "name", "Company", "CustomerName", "Department_Id",
               "ProjectType_Id", "ScheduleStartDate", "DurationSeconds",
               "StartDateTimeUTC", "EndDateTimeUTC", "WorkSeconds",
               "WorkHours", "State", "Status", "CompanyDefault_Id",
               "ProjectStatus_Id", "ProjectType_Id", "ProjectState",
               "WorkPercentComplete", "ItemNumber",
               "PrimaryProjectManager_Id", "LastComment_Id"]
url = url + "?modelProperties=" + ','.join(model_props)
print(url)
resp = requests.get(url, headers=headers)
print(resp.text)
