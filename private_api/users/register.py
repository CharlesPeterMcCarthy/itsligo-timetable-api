import json
import re
import random
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err
import helpers.datetime as dt
import emails.confirm_email as mail

def Handler(event, context):
    data = json.loads(event['body'])
    if 'open' not in data:
        return fnc.ErrorResponse(err.MISSING_DETAILS)
    elif not data['open'] and fnc.ContainsAllData(data, ('studentEmail', 'password')):
        return ClosedRegister(data)
    elif data['open'] and fnc.ContainsAllData(data, ('username', 'password')):
        return OpenRegister(data)
    else:
        return fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckUsernameExists(username, open):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'username': username})
    except:
        return err.DB_QU
    return (err.USERNAME_EXISTS if open else err.EMAIL_EXISTS) if 'Item' in res else {'exists': False}

        ##### OPEN REGISTRATION #####

def OpenRegister(data):
    displayUsername = data['username']
    username = displayUsername.lower()
    hashedPass = fnc.EncryptPassword(data['password'])
    registerAt = dt.GetCurrentDatetime()

    check = CheckUsernameExists(username, True)
    if 'errorText' in check:
        return fnc.ErrorResponse(check)

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={
            'username': username,
            'displayUsername': displayUsername,
            'password': hashedPass,
            'verified': True,
            'open': True,
            'times': {
                'registerAt': registerAt
            }
        })
    except:
        return fnc.ErrorResponse(err.DB_IN)

    authRes = SaveAuthToken(username)
    if 'authToken' not in authRes:
        return fnc.ErrorResponse(authRes)

    return fnc.SuccessResponse(res)

        ##### CLOSED REGISTRATION #####

def ClosedRegister(data):
    email = data['studentEmail'].lower()
    studentID = GetStudentID(email)
    hashedPass = fnc.EncryptPassword(data['password'])
    confirmationCode = GenerateConfirmationCode()
    registerAt = dt.GetCurrentDatetime()

    if not studentID: return fnc.ErrorResponse(err.INVALID_EMAIL)

    check = CheckUsernameExists(studentID, False)
    if 'errorText' in check:
        return fnc.ErrorResponse(check)

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={
            'username': studentID,
            'displayUsername': studentID,
            'email': email,
            'password': hashedPass,
            'verified': False,
            'open': False,
            'times': {
                'registerAt': registerAt
            }
        })
    except:
        return fnc.ErrorResponse(err.DB_IN)

    authRes = SaveAuthToken(studentID)
    if 'authToken' not in authRes: return fnc.ErrorResponse(authRes)

    confirmRes = SaveConfirmationInfo(confirmationCode, studentID)
    if confirmRes['statusCode'] != 200: return confirmRes

    emailRes = mail.SendConfirmEmail(email, confirmationCode)

    return fnc.SuccessResponse(res) if emailRes['statusCode'] == 200 else emailRes

def SaveConfirmationInfo(confirmationCode, studentID):
    try:
        confirmTable = fnc.GetDataTable(tbl.CONFIRM)
        res = confirmTable.put_item(Item={
            'code': confirmationCode,
            'username': studentID,
            'confirmed': False
        })
    except: return fnc.ErrorResponse(err.DB_IN)
    return fnc.SuccessResponse(res)

def SaveAuthToken(username):
    authToken = fnc.GenerateAuthToken()

    try:
        authTable = fnc.GetDataTable(tbl.AUTH)
        res = authTable.put_item(Item={
            'username': username,
            'authToken': authToken
        })
    except:
        return err.DB_IN
    return { 'authToken': authToken }

def GetStudentID(email):
    return email[:9].lower() if re.fullmatch(r'[s/S]\d{8}@mail.itsligo.ie', email) else None

def GenerateConfirmationCode():
    return str("%032x" % random.getrandbits(128))
