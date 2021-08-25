# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
import copy
import re
import uuid
from dataclasses import dataclass, field
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_names: List[str]
    queries: List[Dict]
    regex_queries: List[Dict]
    price: float = field(default=None)
    tag_name: str = field(default=None)
    query: dict = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    headers: Dict = field(init=False, default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141\
                Safari/537.36"
    }
                          )

    def __repr__(self):
        return f"<Item {self.url}, Price {self.price}>"

    def load_price(self) -> float:
        print("Requesting")
        response = requests.get(self.url, headers=self.headers)
        # content = response.content
        print("Finished request")

        soup = BeautifulSoup(response.content, "html.parser")
        for i in range(len(self.tag_names)):
            tag_name = self.tag_names[i]
            query = copy.deepcopy(self.queries[i])
            regex_query = self.regex_queries[i]
            if regex_query is not None:
                query = copy.deepcopy(regex_query)
                for tag in query:
                    print(query[tag])
                    query[tag] = re.compile(query[tag])
            try:
                element = soup.find(tag_name, query)

                string_price = element.text.strip()
                print(query)
                print(element)
                print(string_price)
                prices = string_price.split(',')
                print(prices)
            except AttributeError:
                self.price = None
                continue
            else:
                # string_price = "£4,950.78"
                for string_price in prices:
                    pattern = re.compile(r"([0-9]+,?[0-9]*\.?[0-9]*)")
                    match = pattern.search(string_price)
                    found_price = match.group(1)
                    found_price = found_price.replace(',', '')
                    price = 1e9
                    price = min(float(found_price), price)

                # print(string_price)
                # print(match)
                # print(price)
                self.price = price
                self.tag_name = tag_name
                self.query = query
                return self.price

        if self.price is None:
            raise ValueError("Store not found for this item")

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_names": self.tag_names,
            "price": self.price,
            "queries": self.queries,
            "regex_queries": self.regex_queries,
        }

    def get_id(self):
        return self._id
