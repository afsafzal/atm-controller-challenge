from typing import Optional
import attr

from .card import Card, CardReader


@attr.s
class ATM:

    _card_reader = attr.ib(type=CardReader, default=CardReader())
    _card = attr.ib(type=Optional[Card], default=None)

    def release_card(self) -> Optional[Card]:

        if not self._card:
            print("No card inserted")
            return None

        card = self._card
        self._card = None
        return card

    def insert_card(self):

        if self._card:
            print("There is a card already in use")
            return
        card = self._card_reader.read_card()
        if card:
            self._card = card
        else:
            print("The card is invalid")

    
