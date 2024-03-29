import json
import helpers.functions as fnc
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return fnc.AuthUser(data) if fnc.ContainsAllData(data, ('username', 'authToken')) else fnc.ErrorResponse(err.MISSING_DETAILS)
