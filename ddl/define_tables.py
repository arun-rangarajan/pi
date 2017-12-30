'''
Create tables in sqlite3
'''
import sqlite3

conn = sqlite3.connect('/tmp/pi.db')
cursor = conn.cursor()

def create_table(table_name, table_def):
    cursor.execute('DROP TABLE IF EXISTS ' + table_name)
    cursor.execute(table_def)
    conn.commit()

# table definitions
create_projects = '''
CREATE TABLE projects (
    Id varchar(1000) primary key,
    IdExternal text,
    Name text,
    Company text,
    CustomerName text,
    Department_Id text,
    ProjectType_Id text,
    ScheduleStartDate text,
    DurationSeconds integer,
    StartDateTimeUTC text,
    EndDateTimeUTC text,
    WorkSeconds integer,
    WorkHours real,
    State text,
    Status text,
    CompanyDefault_Id text,
    ProjectStatus_Id text,
    ProjectState text,
    WorkPercentComplete real,
    ItemNumber text,
    PrimaryProjectManager_Id text,
    LastComment_Id text
)
'''
create_table('projects', create_projects)

create_time_entries = '''
CREATE TABLE time_entries (
    Id varchar(1000) primary key,
    ActualHours real,
    ActualTimeString varchar(100),
    ActualTotal real,
    AddedByTimer text,
    BillableHours real,
    BillableTimeString text,
    BillableTotal real,
    Company_Id text,
    Date text,
    Description text,
    ExpenseCode_Id text,
    IdExternal text,
    IsBillable text,
    Project_Id varchar(1000),
    RateBill real,
    RateBurden real,
    TaskWorkPercentComplete text,
    TaskWorkPercentCompleteType_Id text,
    TaskWorkRemainingHours text,
    Task_Id varchar(1000),
    TimeSheet_Id text,
    User_Id text
)
'''
create_table('time_entries', create_time_entries)

create_tasks = '''
CREATE TABLE tasks (
    Id varchar(1000) primary key,
    IdExternal text,
    Name text,
    IsSummaryTask text,
    SummaryTask_Id text,
    IsMilestone text,
    ResourceType_Id text,
    WorkPercentComplete real,
    WorkPercentCompleteType_Id text,
    WorkHours integer,
    WorkSeconds integer,
    ActualStartDateTimeUTC text,
    ActualEndDateTimeUTC text,
    DeadlineDate text,
    WBSCode text,
    StartDateTimeUTC text,
    EndDateTimeUTC text,
    Project_Id text,
    DurationSeconds integer,
    LastComment_Id text
)
'''
create_table('tasks', create_tasks)

create_task_predecessors = '''
CREATE TABLE task_predecessors (
    Id varchar(1000) primary key,
    PredecessorType integer,
    Predecessor_Id text,
    IsLag text,
    Duration integer,
    IdExternal text,
    Task_Id varchar(1000)
)
'''
create_table('task_predecessors', create_task_predecessors)


conn.close()