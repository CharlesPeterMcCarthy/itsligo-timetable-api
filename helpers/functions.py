import decimal
import boto3
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
