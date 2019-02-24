import boto3
import helpers.functions as fnc
import helpers.errors as err
from botocore.exceptions import ClientError

def SendConfirmEmail():
    SENDER = "Charles <chazooo555@gmail.com>"
    RECIPIENT = "charles@campusconnect.ie"
    AWS_REGION = "eu-west-1"
    SUBJECT = "Lambda Python SES Email"
    CHARSET = "UTF-8"

    BODY_TEXT = (
                )

    BODY_HTML = """<html>
    <head></head>
    <body>

    </body>
    </html>"""


    client = boto3.client('ses', region_name="eu-west-1")

    try:
        res = client.send_email(
            Destination={
                'ToAddresses': [ RECIPIENT ],
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
