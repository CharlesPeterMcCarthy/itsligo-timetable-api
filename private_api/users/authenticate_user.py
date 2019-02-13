import json
import helpers.functions as fnc
import helpers.tables as tbl

def Handler(event, context):
    data = json.loads(event['body'])
    return AuthUser(data) if 'StudentID' in data and 'AuthToken' in data else fnc.FormResponse({ 'error': 'Missing Details' })

def AuthUser(data):
    try:
        userTable = fnc.GetDataTable(tbl.AUTH)
        res = userTable.get_item(Key={ 'StudentID': data['StudentID'] })
    except:
        res = { 'error': 'Database error' }

    res = res['Item'] if 'Item' in res else { 'error': 'No user matches that Student ID - Force Logout' }   # Error codes to be setup

    if 'AuthToken' in res:
        if res['AuthToken'] != data['AuthToken']:
            res = { 'error': 'Auth Token is invalid - Force Logout' }    # Error codes to be setup
    if 'error' not in res:
        res = { 'AuthOk': True }

    return fnc.FormResponse(res)
