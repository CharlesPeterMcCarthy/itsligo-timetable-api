import json
import datetime
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckConfirmationCode(data) if 'code' in data else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckConfirmationCode(data):
    confirmedAt = datetime.datetime.now().isoformat()

    try:
        confirmTable = fnc.GetDataTable(tbl.CONFIRM)
        confirmRes = confirmTable.get_item(Key={ 'code': data['code'] })

        if 'Item' in confirmRes:
            res = confirmTable.update_item(
                Key={ 'code': data['code'] },
                UpdateExpression="set #c = :c, #ca = :ca",
                ExpressionAttributeNames={ '#c': 'confirmed', '#ca': 'confirmedAt' },
                ExpressionAttributeValues={ ':c': True, ':ca': confirmedAt },
                ReturnValues="UPDATED_NEW"
            )
        else:
            return fnc.ErrorResponse(err.INVALID_CONFIRM_CODE)

        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            return UpdateUserAsVerified(confirmRes['Item']['username'])
        else:
            return fnc.ErrorResponse(err.DB_QU)

    except:
        return fnc.ErrorResponse(err.DB_UP)

def UpdateUserAsVerified(username):
    verifiedAt = datetime.datetime.now().isoformat()

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.update_item(
            Key={ 'username': username },
            UpdateExpression="set #v = :v, #t.#va = :va",
            ExpressionAttributeNames={ '#v': 'verified', '#t': 'times', '#va': 'verifiedAt' },
            ExpressionAttributeValues={ ':v': True, ':va': verifiedAt },
            ReturnValues="UPDATED_NEW"
        )
    except:
        return fnc.ErrorResponse(err.DB_UP)

    return fnc.SuccessResponse(res)
