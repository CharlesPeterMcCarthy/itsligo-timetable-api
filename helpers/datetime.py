import datetime
import dateutil.tz

def GetCurrentDatetime():
    timezone = dateutil.tz.gettz('Europe/Dublin')
    return datetime.datetime.now(tz=timezone).isoformat()
