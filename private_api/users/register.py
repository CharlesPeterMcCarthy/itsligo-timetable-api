import json
import re
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

    if not studentID:
        return fnc.ErrorResponse(err.INVALID_EMAIL)

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={ 'StudentID': studentID, 'Email': email, 'Name': name, 'Password': hashedPass })
    except:
        return fnc.ErrorResponse(err.DB_IN)

    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        emailRes = mail.SendConfirmEmail(name, email)

        if emailRes['statusCode'] == 200:
            return fnc.SuccessResponse(res)
        else:
            return emailRes

def GetStudentID(email):
    return email[:9].upper() if re.fullmatch(r'[s/S]\d{8}@mail.itsligo.ie', email) else None
