import re
from passlib.hash import pbkdf2_sha512


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_add_matcher = re.compile(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$')
        return re.match(email_add_matcher, email) is not None

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> str:
        return pbkdf2_sha512.verify(password, hashed_password)
