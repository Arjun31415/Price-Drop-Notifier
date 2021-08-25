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
            if response.status_code == 202:
                print('Sending E-mail')
            elif response.status_code >= 400:
                raise SendGirdException(
                    f'Error occurred while sending E-mail Request error: {response.status_code}'
                )
            elif response.status_code >= 500:
                raise SendGirdException(
                    f' Error occurred while sending E-mail Unexpected Error: {response.status_code}'
                )
            return response
        except Exception as e:
            raise e
