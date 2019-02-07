import datetime
import json
from functions.timetable.timetable import GetFullTimetable

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetClassesTomorrow())
    }

def GetClassesTomorrow():
    timetable = GetFullTimetable()
    tomorrowNum = datetime.datetime.today().weekday() + 1
    tomorrow = tomorrowNum if tomorrowNum < 7 else 0
    classes = timetable[tomorrow]['classes']
    return classes if classes else []
