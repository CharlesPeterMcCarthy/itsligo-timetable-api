import datetime
import json
from functions.timetable.timetable import GetFullTimetable

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetClassCount())
    }

def GetClassCount():
    return { 'count': len(GetTodaysClasses()) }

def GetTodaysClasses():
    timetable = GetFullTimetable()
    today = datetime.datetime.today().weekday()
    classes = timetable[today]['classes']
    return classes if classes else []
