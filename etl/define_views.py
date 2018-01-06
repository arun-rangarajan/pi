'''
Views present the data in denormalized form
'''
import sqlite3
import ConfigParser
import os

# ensure property file exists
assert(os.path.exists('db.properties'))

# ensure that sqlite3 database file exists and connect
db_config = ConfigParser.RawConfigParser()
db_config.read('db.properties')
db_file_path = db_config.get('sqlite', 'db.file.path')
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

def create_view(view_name, create_sql):
    cursor.execute('DROP VIEW IF EXISTS ' + view_name)
    cursor.execute(create_sql)
    conn.commit()

count = 0

projects_denorm = '''
create view projects_denorm as 
select 
     p.Name as project_name
    ,p.StartDateTimeUTC
    ,p.EndDateTimeUTC
    ,p.WorkSeconds
    ,p.WorkHours
    ,p.WorkPercentComplete
    ,p.ItemNumber
    ,p.State as project_state
    ,c.Name as company_name
    ,d.Name as dept_name
    ,ps.Name as project_status_name
    ,pm.FirstName || ' ' || pm.LastName as primary_project_manager_name
    ,lc.CommentBody as last_comment
from projects as p 
left outer join companies as c on c.Id = p.CompanyDefault_Id
left outer join departments as d on d.Id = p.Department_Id 
left outer join project_statuses as ps on ps.id = p.ProjectStatus_Id
left outer join users as pm on pm.Id = p.PrimaryProjectManager_Id 
left outer join project_last_comments as lc on lc.Id = p.LastComment_Id
'''
create_view('projects_denorm', projects_denorm)
count += 1

tasks_denorm = '''
create view tasks_denorm as 
select 
     t.Name as task_name
    ,p.Name as project_name
    ,t.IsSummaryTask
    ,summ_t.Name as summary_task_name
    ,t.IsMilestone
    ,tr.IsTaskOwner     
    ,u.FirstName || ' ' || u.LastName as resource_name
    ,t.WorkPercentComplete
    ,t.WorkHours
    ,t.WorkSeconds
    ,t.ActualStartDateTimeUTC
    ,t.ActualEndDateTimeUTC
    ,t.DeadlineDate
    ,t.WBSCode
    ,t.StartDateTimeUTC
    ,t.EndDateTimeUTC
    ,t.DurationSeconds
    ,lc.CommentBody as last_comment
from tasks t 
left outer join tasks summ_t on summ_t.Id = t.SummaryTask_Id 
left outer join task_resources tr on tr.Task_Id = t.Id 
left outer join users u on u.Id = tr.User_id  
left outer join projects p on p.Id = t.Project_Id 
left outer join task_last_comments lc on lc.Id = t.LastComment_Id
'''
create_view('tasks_denorm', tasks_denorm)
count += 1

conn.commit()
print("Created %d views. DB file at %s" % (count, db_file_path))
conn.close()

