import json
import random
import helpers.functions as fnc
import helpers.tables as tbl

def Handler(event, context):
    data = json.loads(event['body'])
    return RegisterUser(data) if 'studentID' in data and 'name' in data and 'password' in data else FormResponse({ 'error': 'Missing Details' })

def RegisterUser(data):
    hashedPass = fnc.EncryptPassword(data['password'])

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={'StudentID': data['studentID'], 'Name': data['name'], 'Password': hashedPass})
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
