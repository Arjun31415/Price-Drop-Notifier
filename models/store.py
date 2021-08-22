from models.model import Model
from typing import Dict
import re


class Store(Model):
    collection = "stores"

    def __init__(
            self, name: str,
            url_prefix: str,
            tag_name: str,
            query: Dict,
            _id: str = None
    ):
        super().__init__(_id=id)
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self.name = name

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
        }

    @classmethod
    def get_by_name(cls, store_name) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like
        "https://www.johnlewis.com/john-lewis-partners-natural-collection-swaledale-wool-11400-king-size-medium-tension-pocket-spring-mattress/p4287158"

        :param url: The item's URL
        :return: a Store object
        """
        pattern = re.compile(r"(https?://.*?/)")
        url_prefix = pattern.search(url).group(1)
        return cls.get_by_url_prefix(url_prefix)
