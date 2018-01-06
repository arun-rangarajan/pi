'''
Fetches data from PI using REST APIs and loads into sqlite DB
'''
import requests
import ConfigParser
import sqlite3
import os
import json
from collections import OrderedDict

# ensure that the properties files exist
assert(os.path.exists('credentials.properties'))
assert(os.path.exists('api.properties'))
assert(os.path.exists('db.properties'))

# ensure that sqlite3 database file exists and connect
db_config = ConfigParser.RawConfigParser()
db_config.read('db.properties')
db_file_path = db_config.get('sqlite', 'db.file.path')
assert(os.path.exists(db_file_path))
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# read credentials
creds_config = ConfigParser.RawConfigParser()
creds_config.read('credentials.properties')

# credentials properties
base_url = creds_config.get('api', 'base.url')
api_token = creds_config.get('api', 'api.token')

# api properties
api_config = ConfigParser.RawConfigParser()
api_config.read('api.properties')

headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'api-token': api_token}

def get_list_with_ordered_items(resp_list):
    '''
    Takes in a list of dictionaries (which are inherently unordered)
    and returns a list of ordered dictionaries
    '''
    if isinstance(resp_list, dict): # single object, so make it a list
        resp_list = [resp_list]
    ordered_list = []
    for obj in resp_list:
        ordered = OrderedDict()
        for k in sorted(obj.keys()):
            ordered[k] = obj[k]
        ordered_list.append(ordered)
    return ordered_list

def extract_base_objects(obj_name):
    '''
    Extract objects that can be obtained as a list from a static URL.
    '''
    url = base_url + \
        api_config.get('api.path', obj_name) + \
        "?modelProperties=" + \
        api_config.get('model.properties', obj_name)
    resp = requests.get(url, headers=headers)
    resp_list = json.loads(resp.text)
    return get_list_with_ordered_items(resp_list)

def extract_sub_objects(obj_name, base_objects, base_obj_ref_field):
    '''
    Extract objects that are dependent on base objects.
    '''
    ordered_list = []
    for base_obj in base_objects:
        base_id = base_obj[base_obj_ref_field]
        if base_id and base_id != 'None':
            url = base_url + \
                api_config.get('api.path', obj_name).format(base_id) + \
                "?modelProperties=" + \
                api_config.get('model.properties', obj_name)
            print(url)
            resp = requests.get(url, headers=headers)
            resp_list = json.loads(resp.text)
            ordered_list.extend(get_list_with_ordered_items(resp_list))
    return ordered_list

def load_objects(obj_name, objects, fields_to_skip=[]):
    cursor.execute('DELETE FROM ' + obj_name)
    props = api_config.get('model.properties', obj_name).split(',')
    props = set(props) - set(fields_to_skip)
    column_names = ['`' + x + '`' for x in props]
    column_names_str = ','.join(column_names)
    sql_fmt = 'INSERT INTO ' + obj_name + '(' + column_names_str + ') VALUES ({})'
    sql_placeholder = sql_fmt.format(','.join(['?'] * len(props)))
    for obj in objects:
        vals = tuple([obj.get(k, None) for k in props])
        cursor.execute(sql_placeholder, vals)
    conn.commit()

def get_row_count(table_name):
    for c, in cursor.execute('SELECT COUNT(*) FROM ' + table_name):
        return c

print("Loading projects...")
projects = extract_base_objects('projects')
load_objects('projects', projects)
print('# of projects inserted = %d' % get_row_count('projects'))

print("Loading time entries...")
time_entries = extract_sub_objects('time_entries', projects, 'Id')
load_objects('time_entries', time_entries)
print('# of time_entries inserted = %d' % get_row_count('time_entries'))

print("Loading tasks (and predecessors)...")
tasks = extract_sub_objects('tasks', projects, 'Id')
task_predecessors = []
for task in tasks:
    preds = task['TaskPredecessors']
    for pred in preds:
        pred['Task_Id'] = task['Id']
    task_predecessors.extend(preds)
    del task['TaskPredecessors']
load_objects('tasks', tasks, ['TaskPredecessors'])
print('# of tasks inserted = %d' % get_row_count('tasks'))
load_objects('task_predecessors', task_predecessors)
print('# of rows task_predecessors inserted = %d' % get_row_count('task_predecessors'))

print("Loading project last comments...")
project_last_comments = extract_sub_objects('last_comments', projects, 'LastComment_Id')
load_objects('project_last_comments', project_last_comments)
print('# of project_last_comments inserted = %d' % get_row_count('project_last_comments'))

print("Loading task last comments...")
task_last_comments = extract_sub_objects('last_comments', tasks, 'LastComment_Id')
load_objects('task_last_comments', task_last_comments)
print('# of task_last_comments inserted = %d' % get_row_count('task_last_comments'))

print("Loading project resources...")
project_resources = extract_sub_objects('project_resources', projects, 'Id')
load_objects('project_resources', project_resources)
print('# of project_resources inserted = %d' % get_row_count('project_resources'))

for entity in ['users', 'companies', 'departments', 'project_types', 'project_statuses',
               'resource_types', 'user_types', 'work_percent_complete_types']:
    print("Loading %s..." % entity)
    objects = extract_base_objects(entity)
    load_objects(entity, objects)
    print('# of %s inserted = %d' % (entity, get_row_count(entity)))

print("Loading task resources...")
task_resources = extract_sub_objects('task_resources', tasks, 'Id')
load_objects('task_resources', task_resources)
print('# of task_resources inserted = %d' % get_row_count('task_resources'))

conn.close()
print('DONE')
