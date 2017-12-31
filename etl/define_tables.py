'''
Create tables in sqlite3
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

def create_table(table_name, table_def):
    cursor.execute('DROP TABLE IF EXISTS ' + table_name)
    cursor.execute(table_def)
    conn.commit()

created_table_count = 0

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
created_table_count += 1

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
created_table_count += 1

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
created_table_count += 1

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
created_table_count += 1

create_project_last_comments = '''
CREATE TABLE project_last_comments (
    Id varchar(1000) primary key,
    ObjectId text,
    CommentBody text,
    UserCreated_Id text,
    CreatedDateTimeUTC text,
    IdExternal text
)
'''
create_table('project_last_comments', create_project_last_comments)
created_table_count += 1

create_task_last_comments = '''
CREATE TABLE task_last_comments (
    Id varchar(1000) primary key,
    ObjectId text,
    CommentBody text,
    UserCreated_Id text,
    CreatedDateTimeUTC text,
    IdExternal text
)
'''
create_table('task_last_comments', create_task_last_comments)
created_table_count += 1

create_task_resources = '''
CREATE TABLE task_resources (
    Id varchar(1000) primary key,
    User_Id text,
    PercentAllocation real,
    Task_Id text,
    IsTaskOwner text,
    WorkSeconds integer,
    IdExternal text,
    ResourceTypeNameForSave text
)
'''
create_table('task_resources', create_task_resources)
created_table_count += 1

create_project_resources = '''
CREATE TABLE project_resources (
    Id varchar(1000) primary key,
    User_Id text,
    Project_Id text,
    IsProjectManager text,
    IsProjectScheduler text,
    PercentAllocationDefault real,
    IdExternal text,
    ResourceTypeNameForSave text
)
'''
create_table('project_resources', create_project_resources)
created_table_count += 1

create_users = '''
CREATE TABLE users (
    Id varchar(1000) primary key,
    FirstName text,
    LastName text,
    Company_Id text,
    Department_Id text,
    ResourceType_Id text,
    ResourceTypeRoleDefault_Id text,
    UserType_Id text
)
'''
create_table('users', create_users)
created_table_count += 1

create_companies='''
CREATE TABLE companies (
    Id varchar(1000) primary key,
    IsActive text,
    CustomFieldValue_Id text,
    Name text,
    IdExternal text
)
'''
create_table('companies', create_companies)
created_table_count += 1

create_departments = '''
CREATE TABLE departments (
    Id varchar(1000) primary key,
    Name text,
    Code text,
    DisplayOrder integer,
    IsActive text,
    IdExternal text
)
'''
create_table('departments', create_departments)
created_table_count += 1

create_project_types = '''
CREATE TABLE project_types (
    Id varchar(1000) primary key,
    Name text,
    Code text,
    `Order` integer,
    IsActive text,
    IdExternal text
)
'''
create_table('project_types', create_project_types)
created_table_count += 1

create_project_statuses = '''
CREATE TABLE project_statuses (
    Id varchar(1000) primary key,
    Name text,
    Icon text,
    DisplayType text,
    Code text,
    `Order` integer,
    IsDefaultValue text,
    IsActive text,
    ChartColor text,
    IdExternal
)
'''
create_table('project_statuses', create_project_statuses)
created_table_count += 1

create_resource_types = '''
CREATE TABLE resource_types (
    Id varchar(1000) primary key,
    Name text,
    Code text,
    `Order` integer,
    IsActive text,
    DefaultTimeExpenseCode_Id text,
    IdExternal text
)
'''
create_table('resource_types', create_resource_types)
created_table_count += 1

create_user_types = '''
CREATE TABLE user_types (
    Id varchar(1000) primary key,
    Name text,
    Code text,
    `Order` integer,
    IsActive text,
    IdExternal text
)
'''
create_table('user_types', create_user_types)
created_table_count += 1

create_work_percent_complete_types = '''
CREATE TABLE work_percent_complete_types (
    Id varchar(1000) primary key,
    Name text,
    WorkPercentComplete real,
    DisplayOrder integer,
    IsActive text,
    EnableKanbanColumn text,
    IdExternal text
)
'''
create_table('work_percent_complete_types', create_work_percent_complete_types)
created_table_count += 1

print("Created %d tables. DB file at %s" % (created_table_count, db_file_path))
conn.close()
