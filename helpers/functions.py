import decimal
import boto3
import json
import random
import helpers.tables as tbl
import helpers.errors as err
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
    return FormResponse(error['code'], { 'errorText': error['errorText'] })

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
    try:
        userTable = GetDataTable(tbl.AUTH)
        res = userTable.get_item(Key={ 'StudentID': data['StudentID'] })
    except: return err.DB_QU

    if 'Item' in res: res = res['Item']
    else: return err.INVALID_STUDENTID

    if 'AuthToken' in res and res['AuthToken'] == data['AuthToken']: return { 'AuthOk': True }
    return err.INVALID_AUTH_TOKEN

def UpdateAuthToken(studentID, authToken):
    try:
        authTable = GetDataTable(tbl.AUTH)
        res = authTable.update_item(
            Key={ 'StudentID': studentID },
            UpdateExpression="set AuthToken = :a",
            ExpressionAttributeValues={ ':a': authToken },
            ReturnValues="UPDATED_NEW"
        )
    except: return err.DB_UP
    return { 'Updated': True }

def ContainsAllData(data, fields):
    return all(d in data for d in fields)
