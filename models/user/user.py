import uuid
from dataclasses import dataclass, field

import models.user.errors as UserErrors
from common.utils import Utils
from models.model import Model


@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: The password
        :return: True if valid, an exception otherwise
        """
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was incorrect.")

        return True

    @classmethod
    def find_by_email(cls, email) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail does not exist')

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        """
                This method registers a user using e-mail and password.
                :param email: user's e-mail (might be invalid)
                :param password: password
                :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail address does not have the right format')

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('This e-mail already exists')
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_db()
        return True

    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
