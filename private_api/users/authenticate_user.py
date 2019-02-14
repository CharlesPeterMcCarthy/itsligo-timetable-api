import json
import helpers.functions as fnc

def Handler(event, context):
    data = json.loads(event['body'])
    return fnc.AuthUser(data) if all(d in data for d in ("StudentID", "AuthToken")) else fnc.FormResponse({ 'error': 'Missing Details' })
