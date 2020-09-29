from typing import Optional, List
import attr
from abc import ABC
from enum import Enum

from .card import Card


@attr.s(frozen=True)
class Bank(ABC):
    '''
    This class is used to implement
    the interface to interace with
    the bank.
    '''

    name = attr.ib(type=str)
    bank_id = attr.ib(type=str)

    @abstractmethod
    def validate_card(self, card: Card, pin: str) -> Optional[User]:
        '''
        This method will call the bank's API to verify
        the card and PIN. If it is correct the method
        returns an object of User that holds information
        about the owner of the card. If not corrrect returns
        None.
        '''
        pass

    @abstractmethod
    def get_balance(self, account: Account) -> int:
        '''
        This method will call the bank's API to get balance
        of an account.
        '''
        pass

    @abstractmethod
    def deposit(self, account: Account, amount: int) -> bool:
        '''
        This method will call the bank's API to deposit amount
        dollars to the account. Returns True if successfull.
        '''
        pass

    @abstractmethod
    def withdraw(self, account: Account, amount: int) -> bool:
        '''
        This method will call the bank's API to withdraw amount
        dollars from the account. Returns True if successfull.
        '''
        pass


@attr.s(frozen=True)
class User:
    '''
    This class holds the information about the user,
    provided by the bank. The bank will use the secret_token
    to make sure the user info is correct.
    '''
    name = attr.ib(type=str)
    user_id = attr.ib(type=str)
    accounts = attr.ib(type=List[Account])
    secret_token = attr.ib(type=str)


class AccountType(Enum):
    CHECKING = 1
    SAVING = 2


@attr.s(frozen=True)
class Account:

    account_id = attr.ib(type=str)
    account_type = attr.ib(type=AccountType)
    user = attr.ib(type=User)
