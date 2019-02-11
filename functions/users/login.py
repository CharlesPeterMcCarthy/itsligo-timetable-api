import json
import random
import helpers.functions as fnc
import helpers.tables as tbl

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if 'studentID' in data and 'password' in data else FormResponse({ 'error': 'Missing Details' })

def CheckLoginDetails(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'StudentID': data['studentID']})
        res = res['Item'] if 'Item' in res else { 'error': 'No user matches that Student ID' }

        if 'Password' in res:
            if data['password'] != res['Password']:
                res = { 'error': 'Password is incorrect'}
            else:
                del res['Password']
        if 'error' not in res:
            res = { 'user': res, 'access-token': GenerateAccessToken() }
    except:
        res = { 'error': 'Unknown error' }

    return FormResponse(res)

def FormResponse(body):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=fnc.DecimalDefault)
    }

def GenerateAccessToken():
    return str("%032x" % random.getrandbits(128))
