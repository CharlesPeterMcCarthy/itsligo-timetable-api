import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckConfirmationCode(data) if 'code' in data else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckConfirmationCode(data):
    try:
        confirmTable = fnc.GetDataTable(tbl.CONFIRM)
        confirmRes = confirmTable.get_item(Key={ 'Code': data['code'] })

        if 'Item' in confirmRes:
            res = confirmTable.update_item(
                Key={ 'Code': data['code'] },
                UpdateExpression="set Confirmed = :c",
                ExpressionAttributeValues={ ':c': True },
                ReturnValues="UPDATED_NEW"
            )
        else:
            return fnc.ErrorResponse(err.INVALID_CONFIRM_CODE)

        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            return UpdateUserAsVerified(confirmRes['Item']['StudentID'])
        else:
            return fnc.ErrorResponse(err.DB_QU)

    except:
        return fnc.ErrorResponse(err.DB_UP)

def UpdateUserAsVerified(studentID):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.update_item(
            Key={ 'StudentID': studentID },
            UpdateExpression="set Verified = :v",
            ExpressionAttributeValues={ ':v': True },
            ReturnValues="UPDATED_NEW"
        )
    except:
        return fnc.ErrorResponse(err.DB_UP)

    return fnc.SuccessResponse(res)
