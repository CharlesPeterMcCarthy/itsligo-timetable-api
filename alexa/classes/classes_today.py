import datetime
import json
from public_api.timetable.timetable import GetFullTimetable

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetClassesToday())
    }

def GetClassesToday():
    timetable = GetFullTimetable()
    today = datetime.datetime.today().weekday()
    classes = timetable[today]['classes']
    return classes if classes else []
