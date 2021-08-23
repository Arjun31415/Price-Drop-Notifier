import re


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_add_matcher = re.compile(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$')
        return re.match(email_add_matcher, email) is not None
