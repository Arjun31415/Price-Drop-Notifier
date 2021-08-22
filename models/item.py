# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

import re
import uuid
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from common.database import Database

from .model import Model


class Item(Model):
    collection = "Items"

    def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None):

        super().__init__(_id=_id)
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141\
            Safari/537.36"
        }
        self.price: float = None

    def __repr__(self):
        return f"<Item {self.url}, Price {self.price}>"

    def load_price(self) -> float:
        print("Requesting")
        response = requests.get(self.url, headers=self.headers)
        # content = response.content
        print("Finished request")

        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()
        # string_price = "£4,950.78"
        pattern = re.compile(r"([0-9]+,?[0-9]*\.?[0-9]*)")
        match = pattern.search(string_price)

        found_price = match.group(1)
        found_price = found_price.replace(',', '')
        price = float(found_price)
        # print(string_price)
        # print(match)
        # print(price)
        self.price = price
        return self.price

    def json(self) -> Dict:
        return{
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query,
        }
