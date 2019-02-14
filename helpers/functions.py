import decimal
import boto3
import json
import random
import helpers.tables as tbl
from passlib.context import CryptContext

def DecimalDefault(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError

def GetDataTable(tableName):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
    except:
        return { 'error': 'Unable to connect to database' }
    return table

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def EncryptPassword(password):
    return pwd_context.encrypt(password)

def VerifyPassword(password, hashedPass):
    return pwd_context.verify(password, hashedPass)

def FormResponse(body):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=DecimalDefault)
    }

def GenerateAccessToken():
    return str("%032x" % random.getrandbits(128))

def AuthUser(data):
    try:
        userTable = GetDataTable(tbl.AUTH)
        res = userTable.get_item(Key={ 'StudentID': data['StudentID'] })
    except:
        res = { 'error': 'Database error' }

    res = res['Item'] if 'Item' in res else { 'error': 'No user matches that Student ID - Force Logout' }   # Error codes to be setup

    if 'AuthToken' in res:
        if res['AuthToken'] != data['AuthToken']:
            res = { 'error': 'Auth Token is invalid - Force Logout' }    # Error codes to be setup
    if 'error' not in res:
        res = { 'AuthOk': True }

    return FormResponse(res)
