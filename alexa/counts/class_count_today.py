import datetime
import json
from public_api.timetable.timetable import GetFullTimetable
from alexa.classes.classes_today import GetClassesToday

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetClassCountToday())
    }

def GetClassCountToday():
    return { 'count': len(GetClassesToday()) }
