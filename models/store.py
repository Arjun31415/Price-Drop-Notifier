import re
import uuid
from dataclasses import dataclass, field
from typing import Dict

from models.model import Model


@dataclass
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    regex_query: Dict = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
            "regex_query": self.regex_query
        }

    @classmethod
    def get_by_name(cls, store_name) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix) -> list["Store"]:
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_many_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> list["Store"]:
        """
        Return a store from a url like
        "https://www.johnlewis.com/john-lewis-partners-natural-collection-swaledale-wool-11400-king-size-medium-tension-pocket-spring-mattress/p4287158"

        :param url: The item's URL
        :return: a Store object
        """
        pattern = re.compile(r"(https?://.*?/)")
        url_prefix = pattern.search(url).group(1)
        return cls.get_by_url_prefix(url_prefix)
