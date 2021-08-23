import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Union

from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default="users");
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail does not exist')

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail address does not have the right format')

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('This e-mail already exists')
        except UserErrors.UserNotFoundError:
            User(email, password).save_to_db()

    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
