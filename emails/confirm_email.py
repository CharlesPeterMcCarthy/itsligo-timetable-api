import boto3
import helpers.functions as fnc
import helpers.errors as err
import emails.email_info as info
from botocore.exceptions import ClientError

def SendConfirmEmail(RECIPIENT_NAME, RECIPIENT_EMAIL, CONFIRM_CODE):
    SENDER = FormSenderDetails(info.SENDER_NAME, info.SENDER_EMAIL)
    CONFIRM_URL = ConfigureConfirmationURL(CONFIRM_CODE)
    SUBJECT = "ITSligo Timetable"
    CHARSET = "UTF-8"

    BODY_TEXT = (
        "Welcome" + RECIPIENT_NAME + "\r\n"
        "Please confirm your email by copying and pasting the "
        "following URL into your browser: \r\n" + CONFIRM_URL
    )

    BODY_HTML = "<html>\
        <head></head>\
        <body>\
            <h2>ITSligo Timetable</h2>\
            <p>Welcome " + RECIPIENT_NAME + "!\
            <p>Please confirm your email by clicking on the following URL: </p>\
            <a href='" + CONFIRM_URL + "'>Confirm Email</a>\
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
    return f'{name} <{email}>'

def ConfigureConfirmationURL(confirmationCode):
    return f'{info.SITE_URL}/confirm/{confirmationCode}'
