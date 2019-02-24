import boto3
import helpers.functions as fnc
import helpers.errors as err
import emails.email_info as email
from botocore.exceptions import ClientError

def SendConfirmEmail(RECIPIENT_NAME, RECIPIENT_EMAIL):
    SENDER = FormSenderDetails(email.SENDER_NAME, email.SENDER_EMAIL)
    SUBJECT = "ITSligo Timetable"
    CHARSET = "UTF-8"

    BODY_TEXT = (
                    "Welcome" + RECIPIENT_NAME + "\r\n"
                    "Please confirm your email by copying and pasting the "
                    "following URL into your browser: \r\n" + email.SITE_URL
                )

    BODY_HTML = "<html>\
        <head></head>\
        <body>\
            <h2>ITSligo Timetable</h2>\
            <p>Welcome " + RECIPIENT_NAME + "!\
            <p>Please confirm your email by clicking on the following URL: </p>\
            <a href='" + email.SITE_URL + "'>Link to localhost</a>\
        </body>\
    </html>"

    client = boto3.client('ses', region_name="eu-west-1")

    try:
        res = client.send_email(
            Destination={
                'ToAddresses': [ RECIPIENT_EMAIL ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        return fnc.ErrorResponse(err.EMAIL_CON)
    else:
        return fnc.SuccessResponse(res)

def FormSenderDetails(name, email):
    return name + " <" + email + ">"
