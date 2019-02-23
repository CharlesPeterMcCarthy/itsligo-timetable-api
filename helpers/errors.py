    #General
UNKNOWN = { 'code': 400, 'errorText': 'An Unknown Error Occurred' }
MISSING_DETAILS = { 'code': 401, 'errorText': 'Details are missing from the request body' }
INVALID_AUTH_TOKEN = { 'code': 403, 'errorText': 'Invalid Auth Token' }

INVALID_STUDENTID = { 'code': 401, 'errorText': 'No user matches that Student ID' }
WRONG_PASSWORD = { 'code': 401, 'errorText': 'Password is Incorrect' }

TIMETABLE_UPDATE = { 'code': 304, 'errorText': 'Your timetable could not be updated' }
TIMETABLE_ACCESS = { 'code': 404, 'errorText': 'Unable to access ITSligo Timetable' }
