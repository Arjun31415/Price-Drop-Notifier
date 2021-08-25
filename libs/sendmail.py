import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List, Union
from requests import Response, post


class SendGirdException(Exception):
    def __init__(self, message: str):
        self.message = message


class SendGrid:
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)
    FROM_TITLE = 'Pricing Alerts'
    FROM_EMAIL = 'pricingalerts@gmail.com'

    @classmethod
    def send_email(cls, email: Union[str, list[str]], subject: str, text: str, html: str) -> Response:
        if cls.SENDGRID_API_KEY is None:
            cls.SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)
            if cls.SENDGRID_API_KEY is None:
                raise SendGirdException("API key is not set in .env")
        message = Mail(
            from_email=cls.FROM_EMAIL,
            to_emails=email,
            subject=subject,
            plain_text_content=text,
            html_content=html)
        try:
            sg = SendGridAPIClient(cls.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            if response.status_code != 200 and response.status_code != 202:
                raise SendGirdException('An error occurred while sending the email')
            elif response.status_code == 202:
                print('Sending E-mail')
            return response
        except Exception as e:
            raise e
