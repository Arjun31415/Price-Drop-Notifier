import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()
message = Mail(
    from_email='arjunp0710@gmail.com',
    to_emails='arnavp3007@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>Please reply if u got this \n from Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    print(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
