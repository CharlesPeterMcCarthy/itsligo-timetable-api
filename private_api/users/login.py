import json
import random
import helpers.functions as fnc
import helpers.tables as tbl

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if 'studentID' in data and 'password' in data else fnc.FormResponse({ 'error': 'Missing Details' })

def CheckLoginDetails(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'StudentID': data['studentID']})
        res = res['Item'] if 'Item' in res else { 'error': 'No user matches that Student ID' }

        if 'Password' in res:
            if fnc.VerifyPassword(fnc.EncryptPassword(data['password']), res['Password']):
                del res['Password']
            else:
                res = { 'error': 'Password is incorrect'}
        if 'error' not in res:
            res = { 'user': res, 'access-token': GenerateAccessToken() }
    except:
        res = { 'error': 'Unknown error' }

    return fnc.FormResponse(res)

def GenerateAccessToken():
    return str("%032x" % random.getrandbits(128))
