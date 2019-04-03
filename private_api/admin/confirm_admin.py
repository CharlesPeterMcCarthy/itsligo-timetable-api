import json
import helpers.functions as fnc
import helpers.errors as err
import helpers.admin as admin

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('username', 'authToken')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    isAdmin = admin.CheckIsAdmin(data['username'])
    if 'isAdmin' not in isAdmin or not isAdmin['isAdmin']: return fnc.ErrorResponse(isAdmin)
    return fnc.SuccessResponse({'adminConfirmed': True})
