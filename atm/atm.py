from typing import Optional
import attr

from .card import Card, CardReader
from .bank import Bank, User, Account


@attr.s
class Session:

    card = attr.ib(type=Optional[Card], default=None)
    user = attr.ib(type=Optional[User], default=None)
    account = attr.ib(type=Optional[Account], default=None)


@attr.s
class ATM:

    _card_reader = attr.ib(type=CardReader)
    _bank = attr.ib(type=Bank)
    _session = attr.ib(type=Session, default=Session())

    def release_card(self) -> Optional[Card]:
        if not self._session.card:
            print("No card inserted")
            return None

        card = self._session.card
        self._session = Session()
        return card

    def insert_card(self):

        if self._session.card:
            print("There is a card already in use")
            return

        assert self._session.user == None
        
        card = self._card_reader.read_card()
        if card:
            self._session.card = card
        else:
            print("The card is invalid")

    def validate_pin(self, pin: str) -> bool:
        if not self._session.card:
            print("No card inserted")
            return False
        if self._session.user:
            print("User is already logged in")
            return False

        user = self._bank.validate_card(self._session.card, pin)
        if not user:
            print("Invalid PIN")
            return False
        self._session.user = user
        return True

    def get_all_accounts(self) -> List[Account]:

        if not self._session.user:
            print("No user logged in")
            return []

        return self._session.user.accounts

    def select_account(self, account_id: str):

        if not self._session.user:
            print("No user logged in")
            return False

        account = None
        for acc in self._session.user.accounts:
            if acc.account_id = account_id:
                account = acc
                break
        if not account:
            print("The account does not belong to the logged in user")
            return False

        self._session.account = account
        return True


    
