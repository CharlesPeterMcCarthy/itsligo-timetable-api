import datetime
import json
from functions.timetable.timetable import GetFullTimetable
from functions.classes.classes_today import GetClassesToday

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetClassCountToday())
    }

def GetClassCountToday():
    return { 'count': len(GetClassesToday()) }
