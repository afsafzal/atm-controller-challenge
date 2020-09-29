from typing import Optional, List
import attr
from abc import ABC

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
            assert self.account.user == self.user
        if self.user:
            assert self.card != None

@attr.s
class ATM:

    _card_reader = attr.ib(type=CardReader)
    _bank = attr.ib(type=Bank)
    _session = attr.ib(type=Session, default=Session())
    _money_bin = attr.ib(type=Optional[MoneyBin], default=None)

    def release_card(self) -> Optional[Card]:
        self._session.validate()

        if not self._session.card:
            print("No card inserted")
            return None

        card = self._session.card
        self._session = Session()
        return card

    def insert_card(self):
        self._session.validate()

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
        self._session.validate()

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
        self._session.validate()

        if not self._session.user:
            print("No user logged in")
            return []

        return self._session.user.accounts

    def select_account(self, account_id: str):
        self._session.validate()

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

    def get_balance(self) -> int:
        self._session.validate()
        
        if not self._session.account:
            print("No account selected")
            return -1

        return self._bank.get_balance(self._session.account)

    def deposit(self, amount: int) -> bool:
        self._session.validate()

        if not self._session.account:
            print("No account selected")
            return False

        if self._money_bin and not self._money_bin.can_deposit(amount):
            print("Not enough room for the bills in the ATM.")
            return False

        if self._money_bin and not self._money_bin.deposit(amount):
            print("The amount of bills did not match the amount specified.")
            return False

        success = self._bank.deposit(self._session.account, amount)
        if not success:
            print("Deposit unsuccessful. Take back your money.")
            if self._money_bin:
                self._money_bin.withdraw(amount)
            return False
        return True

    def withdraw(self, amount: int) -> bool:
        self._session.validate()

        if not self._session.account:
            print("No account selected")
            return False

        if self._money_bin and not self._money_bin.can_withdraw(amount):
            print("Not enough bills in the ATM.")
            return False

        success = self._bank.withdraw(self._session.account, amount)
        if not success:
            print("Withdrawal unsuccessful.")
            return False

        if self._money_bin and not self._money_bin.withdraw(amount):
            print("Something went wrong.")
            # We should cancel transaction and return the money
            attempts = 0
            while not success and attempts < 5:
                success = self._bank.deposit(self._session.account, amount)
                attempts += 1
            if not successful:
                print("The return of your money was unsuccessful.
                       Please take the printed receipt to your bank to
                       fix your account balance")
            return False

        return True

