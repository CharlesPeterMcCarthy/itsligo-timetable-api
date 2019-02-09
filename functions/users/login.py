import json
import boto3
import random
from helpers import DecimalDefault

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if 'studentID' in data and 'password' in data else { 'error': 'Missing Details' }

def CheckLoginDetails(data):
    try:
        userTable = GetUserTable()
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
        res = { 'error': 'unknown error' }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(res, default=DecimalDefault)
    }

def GetUserTable():
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("Users2")
    except:
        return { 'error': 'Unable to connect to database' }
    return table

def GenerateAccessToken():
    return str("%032x" % random.getrandbits(128))
