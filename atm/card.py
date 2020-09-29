import attr
from datetime import date
from abc import ABC


@attr.s(frozen=True)
class Card:

    number = attr.ib(type=str)
    cvv = attr.ib(type=str)
    expiration_date = attr.ib(type=date)

    @number.validator
    def number_validator(self, attribute, value):
        if len(value) != 16:
            raise ValueError("The card number is invalid")

    @expiration_date.validator
    def date_validator(self, attribute, value):
        today = date.today()
        if value.year < today.year:
            raise ValueError("The card is expired")
        if value.year == today.year and value.month < today.month:
            raise ValueError("The card is expired")

@attr.s(frozen=True)
class CardReader(ABC):

    @abstractmethod
    def read_card(self) -> Card:
        '''
        The card reader should implement this
        to read the card, create a Card object
        and return it.
        '''
        pass
