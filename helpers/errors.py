UNKNOWN = { 'code': 400, 'errorText': 'An Unknown Error Occurred' }
MISSING_DETAILS = { 'code': 401, 'errorText': 'Details are missing from the request body' }
INVALID_AUTH_TOKEN = { 'code': 403, 'errorText': 'Invalid Auth Token' }
NO_AUTH_TOKEN = { 'code': 403, 'errorText': 'No Auth Token associated with your account' }

NO_TIMETABLE_RETURN_DATA = { 'code': 401, 'errorText': 'Modules, breaks or both must be included' }

INVALID_STUDENTID = { 'code': 401, 'errorText': 'No user matches that Student ID' }
WRONG_PASSWORD = { 'code': 401, 'errorText': 'Password is Incorrect' }
UNVERIFIED_USER = { 'code': 401, 'errorText': 'Your email has not been verified yet' }

NOT_ADMIN = { 'code': 401, 'errorText': 'Not an Admin account' }

TIMETABLE_UPDATE = { 'code': 304, 'errorText': 'Your timetable could not be updated' }
TIMETABLE_ACCESS = { 'code': 404, 'errorText': 'Unable to access ITSligo Timetable' }

EMAIL_CON = { 'code': 400, 'errorText': 'Failed to send confirmation email' }
INVALID_EMAIL = { 'code': 400, 'errorText': 'Email is invalid - Must be an ITSligo student email address' }

INVALID_CONFIRM_CODE = { 'code': 400, 'errorText': 'Confirmation code is invalid' }

DB = { 'code': 400, 'errorText': 'A database error occurred' }
DB_QU = { 'code': 400, 'errorText': 'An error occurred while querying the database' }
DB_IN = { 'code': 400, 'errorText': 'An error occurred while inserting data into the database' }
DB_UP = { 'code': 400, 'errorText': 'An error occurred while updating data in the database' }
