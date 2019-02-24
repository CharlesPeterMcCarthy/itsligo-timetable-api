import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err
import emails.confirm_email as email

def Handler(event, context):
    data = json.loads(event['body'])
    return RegisterUser(data) if fnc.ContainsAllData(data, ('studentID', 'name', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def RegisterUser(data):
    hashedPass = fnc.EncryptPassword(data['password'])

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.put_item(Item={ 'StudentID': data['studentID'], 'Name': data['name'], 'Password': hashedPass })
    except:
        return fnc.ErrorResponse(err.DB_IN)

    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        emailRes = email.SendConfirmEmail()

        if emailRes['statusCode'] == 200:
            return fnc.SuccessResponse(res)
        else:
            return emailRes
