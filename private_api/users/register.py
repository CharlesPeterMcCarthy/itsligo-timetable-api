import json
import re
import random
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err
import emails.confirm_email as mail

def Handler(event, context):
    data = json.loads(event['body'])
    return RegisterUser(data) if fnc.ContainsAllData(data, ('studentEmail', 'name', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def RegisterUser(data):
    email = data['studentEmail'].lower()
    studentID = GetStudentID(email)
    name = data['name']
    hashedPass = fnc.EncryptPassword(data['password'])
    confirmationCode = GenerateConfirmationCode()

    if not studentID: return fnc.ErrorResponse(err.INVALID_EMAIL)

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={
            'StudentID': studentID,
            'Email': email,
            'Name': name,
            'Password': hashedPass,
            'Verified': False
        })
    except: return fnc.ErrorResponse(err.DB_IN)

    authRes = SaveAuthToken(studentID)
    if 'AuthToken' not in authRes: return fnc.ErrorResponse(authRes)

    confirmRes = SaveConfirmationInfo(confirmationCode, studentID)
    if confirmRes['statusCode'] != 200: return confirmRes

    emailRes = mail.SendConfirmEmail(name, email, confirmationCode)

    return fnc.SuccessResponse(res) if emailRes['statusCode'] == 200 else emailRes

def SaveConfirmationInfo(confirmationCode, studentID):
    try:
        confirmTable = fnc.GetDataTable(tbl.CONFIRM)
        res = confirmTable.put_item(Item={
            'Code': confirmationCode,
            'StudentID': studentID,
            'Confirmed': False
        })
    except: return fnc.ErrorResponse(err.DB_IN)
    return fnc.SuccessResponse(res)

def SaveAuthToken(studentID):
    authToken = fnc.GenerateAuthToken()
    try:
        authTable = fnc.GetDataTable(tbl.AUTH)
        res = authTable.put_item(Item={
            'StudentID': studentID,
            'AuthToken': authToken
        })
    except: return err.DB_IN
    return { 'AuthToken': authToken }

def GetStudentID(email):
    return email[:9].upper() if re.fullmatch(r'[s/S]\d{8}@mail.itsligo.ie', email) else None

def GenerateConfirmationCode():
    return str("%032x" % random.getrandbits(128))
