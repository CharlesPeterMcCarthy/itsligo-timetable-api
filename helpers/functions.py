import decimal
import boto3
import json
import random
import helpers.tables as tbl
import helpers.errors as err
import helpers.datetime as dt
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

def SuccessResponse(body):
    return FormResponse(200, body)

def ErrorResponse(error):
    return FormResponse(error['code'], error)

def FormResponse(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=DecimalDefault)
    }

def GenerateAuthToken():
    return str("%032x" % random.getrandbits(128))

def AuthUser(data):
    username = data['username'].lower()

    try:
        authTable = GetDataTable(tbl.AUTH)
        res = authTable.get_item(Key={'username': username})
    except: return err.DB_QU

    if 'Item' in res: res = res['Item']
    else: return err.NO_AUTH_TOKEN

    if 'authToken' in res and res['authToken'] == data['authToken']: return { 'authOk': True }
    return err.INVALID_AUTH_TOKEN

def UpdateAuthToken(username, authToken):
    username = username.lower()

    try:
        authTable = GetDataTable(tbl.AUTH)
        res = authTable.update_item(
            Key={ 'username': username },
            UpdateExpression="set authToken = :a",
            ExpressionAttributeValues={ ':a': authToken },
            ReturnValues="UPDATED_NEW"
        )
    except: return err.DB_UP
    return { 'updated': True }

def UpdateLastAction(username):
    username = username.lower()
    lastAction = dt.GetCurrentDatetime()

    try:
        userTable = GetDataTable(tbl.USERS)
        res = userTable.update_item(
            Key={'username': username},
            UpdateExpression="set #t.#l = :d",
            ExpressionAttributeNames={'#t': 'times', '#l': 'lastAction'},
            ExpressionAttributeValues={':d': lastAction},
            ReturnValues="NONE"
        )
    except: return err.DB_UP
    return { 'updated': True }

def ContainsAllData(data, fields):
    return all(d in data for d in fields)
