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

# ensure that sqlite3 database file exists and connect
db_file_path = '/tmp/pi.db'
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
        url = base_url + \
            api_config.get('api.path', obj_name).format(base_obj[base_obj_ref_field]) + \
            "?modelProperties=" + \
            api_config.get('model.properties', obj_name)
        print(url)
        resp = requests.get(url, headers=headers)
        resp_list = json.loads(resp.text)
        ordered_list.extend(get_list_with_ordered_items(resp_list))
    return ordered_list

def load_objects(obj_name, objects):
    cursor.execute('DELETE FROM ' + obj_name)
    obj0 = objects[0]
    sql = 'INSERT INTO ' + obj_name + '(' + ','.join(obj0.keys()) + \
        ') VALUES (' + ','.join(['?'] * len(obj0)) + ')'
    #print(sql)
    cursor.executemany(sql, [o.values() for o in objects])
    conn.commit()

def get_row_count(table_name):
    for c, in cursor.execute('SELECT COUNT(*) FROM ' + table_name):
        return c


projects = extract_base_objects('projects')
load_objects('projects', projects)
print('# of rows inserted =', get_row_count('projects'))

time_entries = extract_sub_objects('time_entries', projects, 'Id')
load_objects('time_entries', time_entries)
print('# of rows inserted =', get_row_count('time_entries'))

conn.close()
