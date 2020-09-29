from typing import Optional, List
import attr
from abc import ABC, abstractmethod

from .card import Card, CardReader
from .bank import Bank, User, Account


class MoneyBin(ABC):
    '''
    In the future, this class implements the
    API to interact with the money bin.
    '''

    @abstractmethod
    def deposit(self, amount: int):
        '''
        Puts amount number dollar bills in the bin
        if it fits, otherwise returns the money.
        '''
        pass

    @abstractmethod
    def withdraw(self, amount: int):
        '''
        If the requested amount of dollar bills
        exists in the bin, deducts the amount
        from the balance of the bin, otherwise
        return an Error.
        '''
        pass

    @abstractmethod
    def can_withdraw(self, amount: int) -> bool:
        '''
        If the requested amount of dollar bills
        exists in the bin, return True, otherwise
        return False.
        '''
        pass

    @abstractmethod
    def can_deposit(self, amount: int) -> bool:
        '''
        If the requested amount of dollar bills
        fits in the bin, return True, otherwise
        return False.
        '''
        pass


@attr.s
class Session:
    '''
    This class keeps an ongoing session
    of interaction with the ATM.
    '''

    card = attr.ib(type=Optional[Card], default=None)
    user = attr.ib(type=Optional[User], default=None)
    account = attr.ib(type=Optional[Account], default=None)

    def account_operation_allowed(self) -> bool:
        if self.card and self.user and self.account:
            return True
        return False

    def validate(self):
        '''
        This method can be used to make sure the session
        has not been tampered with and is valid.
        '''
        if self.account:
            assert self.user
            assert self.account in self.user.accounts
        if self.user:
            assert self.card is not None


@attr.s
class ATM:
    '''
    The class representing the ATM that consists
    of a card reader, a connected banking system,
    a running session, and potentially a money bin.
    '''

    _card_reader = attr.ib(type=CardReader)
    _bank = attr.ib(type=Bank)
    _session = attr.ib(type=Session, default=attr.Factory(Session))
    _money_bin = attr.ib(type=Optional[MoneyBin], default=None)

    def release_card(self) -> Optional[Card]:
        self._session.validate()

        if not self._session.card:
            print("No card inserted")
            return None

        card = self._session.card
        # The previous session is over
        self._session = Session()
        return card

    def insert_card(self) -> int:
        self._session.validate()

        if self._session.card:
            print("There is a card already in use")
            return -1

        card = self._card_reader.read_card()
        if card:
            self._session.card = card
            return 0
        else:
            # The card reader was unable to read the card
            print("The card is invalid")
            return -2

    def get_card_number(self) -> str:
        self._session.validate()

        if not self._session.card:
            return ""

        return self._session.card.number

    def validate_pin(self, pin: str) -> int:
        self._session.validate()

        if not self._session.card:
            print("No card inserted")
            return -1
        if self._session.user:
            print("User is already logged in")
            return -2

        user = self._bank.validate_card(self._session.card, pin)
        if not user:
            print("Invalid PIN")
            return -3
        self._session.user = user
        return 0

    def get_all_accounts(self) -> List[Account]:
        self._session.validate()

        if not self._session.user:
            print("No user logged in")
            return []

        return self._session.user.accounts

    def select_account(self, account_id: str):
        self._session.validate()

        if not self._session.user:
            print("No user logged in")
            return -1

        account = None
        # Make sure the given account id belongs to the logged in user
        for acc in self._session.user.accounts:
            if acc.account_id == account_id:
                account = acc
                break
        if not account:
            print("The account does not belong to the logged in user")
            return -2

        self._session.account = account
        return 0

    def get_account_id(self) -> str:
        self._session.validate()

        if not self._session.account:
            print("No account selected")
            return ''

        return self._session.account.account_id

    def get_balance(self) -> int:
        self._session.validate()

        if not self._session.account:
            print("No account selected")
            return -1

        return self._bank.get_balance(self._session.user,
                                      self._session.account)

    def deposit(self, amount: int) -> int:
        self._session.validate()

        if amount <= 0:
            print("Invalid amount")
            return -5

        if not self._session.account:
            print("No account selected")
            return -1

        # If there's a money bin check if it has enough capacity
        if self._money_bin and not self._money_bin.can_deposit(amount):
            print("Not enough room for the bills in the ATM.")
            return -2

        # If there's a money bin put the money from user to the bin
        if self._money_bin and not self._money_bin.deposit(amount):
            print("The amount of bills did not match the amount specified.")
            return -3

        success = self._bank.deposit(self._session.user,
                                     self._session.account,
                                     amount)
        if not success:
            print("Deposit unsuccessful. Take back your money.")
            # If there's a money bin return the money to the user
            if self._money_bin:
                self._money_bin.withdraw(amount)
            return -4
        return 0

    def withdraw(self, amount: int) -> int:
        self._session.validate()

        if amount <= 0:
            print("Invalid amount")
            return -5

        if not self._session.account:
            print("No account selected")
            return -1

        # If there's a money bin make sure it has enought bills
        if self._money_bin and not self._money_bin.can_withdraw(amount):
            print("Not enough bills in the ATM.")
            return -2

        success = self._bank.withdraw(self._session.user,
                                      self._session.account,
                                      amount)
        if not success:
            print("Withdrawal unsuccessful.")
            return -4

        if self._money_bin and not self._money_bin.withdraw(amount):
            # The money is deducted from user's account but money bin failed
            print("Something went wrong.")
            # We should cancel transaction and return the money
            attempts = 0
            while not success and attempts < 5:
                success = self._bank.deposit(self._session.user,
                                             self._session.account,
                                             amount)
                attempts += 1
            if not success:
                # In this case the user should take the evidence/receipt
                # to later make a dispute, and ask the bank to return
                # their money.
                print("The return of your money was unsuccessful."
                      "Please take the printed receipt to your bank to"
                      "fix your account balance")
            return -3

        return 0
