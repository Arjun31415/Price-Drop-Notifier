# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
import uuid
from dataclasses import dataclass, field
from typing import Dict

from libs.sendmail import SendGrid
from models.item import Item
from models.model import Model
from models.user import User


@dataclass(eq=False)
class Alert(Model):
    """
         Class for Alerts on `Item` object
         (`<models.item>`)
    """
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email,
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
            resp = SendGrid.send_email(
                email=self.user_email,
                subject='test',
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price '
                     f'is {self.item.price}. Check your item out <a href="{self.item.url}>here</a>.</p>',
            )
            print(resp.status_code)
