# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

from typing import Dict

from models.item import Item
from models.model import Model


class Alert(Model):
    collection = "Alerts"
    """
    Class for Alerts on `Item` object
    (`<models.item>`)
    """

    def __init__(self, item_id: str, price_limit: float, _id: str = None) -> None:
        """
            constructor
            :param item_id: the `Item`'s id for which the alert is created
            :param price_limit: the price below which the user has to be alerted
            :param _id: he `id` of the `Alert` object. Defaults to None.
        """
        super().__init__(_id=_id)
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.price_limit = price_limit
        # self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price <= self.price_limit:
            print(
                f"Item {self.item} has reached \
                a price under {self.price_limit}. \
                Latest price:{self.item.price}\
                "
            )
