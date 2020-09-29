import attr
from datetime import date

from atm.card import CardReader, Card
from atm.bank import Bank, User, Account, AccountType
from atm.atm import MoneyBin


ACCOUNT1_CH = Account('0001', AccountType.CHECKING)
ACCOUNT1_SA = Account('0002', AccountType.SAVING)
USER1 = User('Jane Doe', '001', [ACCOUNT1_CH, ACCOUNT1_SA], 'uasdhfua')
CARD1 = Card('1234567890111213', '111', date(2100, 12, 1))


class DummyBank(Bank):

    def __init__(self):
        super().__init__("Dummy", "1234")
        self.cards = {CARD1.number: {'PIN': '1234',
                                     'user': USER1.user_id},
                     }
        self.users = {USER1.user_id: USER1}
        self.accounts = {ACCOUNT1_CH.account_id: 1000,
                         ACCOUNT1_SA.account_id: 500
                         }

    def validate_card(self, card: Card, pin: str):
        if not card.number in self.cards:
            return None

        info = self.cards[card.number]
        if info['PIN'] != pin:
            return None
        return self.users[info['user']]


    def validate_user_account(self, user: User, account: Account) -> bool:
        if not user.user_id in self.users or\
                self.users[user.user_id].secret_token != user.secret_token:
            return False

        if not account.account_id in self.accounts:
            return False

        u = self.users[user.user_id]
        if not account.account_id in [a.account_id for a in u.accounts]:
            return False

        return True

    def get_balance(self, user: User, account: Account) -> int:
        if not self.validate_user_account(user, account):
            return -1

        return self.accounts[account.account_id]

    def deposit(self, user: User, account: Account, amount: int) -> bool:
        if not self.validate_user_account(user, account):
            return False

        self.accounts[account.account_id] += amount
        return True

    def withdraw(self, user: User, account: Account, amount: int) -> bool:
        if not self.validate_user_account(user, account):
            return False

        balance = self.accounts[account.account_id]
        if balance < amount:
            return False
        self.accounts[account.account_id] -= amount
        return True


class DummyCardReader(CardReader):

    def read_card(self) -> Card:
        return CARD1

class BadCardReader(CardReader):

    def read_card(self) -> Card:
        return None

class DummyMoneyBin(MoneyBin):

    def __init__(self):
        self.max_capacity = 2000
        self.current_holding = 1000
        super().__init__()

    def deposit(self, amount: int):

        if amount + self.current_holding <= self.max_capacity:
            self.current_holding += amount
            return True
        return False

    def withdraw(self, amount: int):

        if amount > self.current_holding:
            return False

        self.current_holding -= amount
        return True

    def can_withdraw(self, amount: int) -> bool:
        return amount <= self.current_holding

    def can_deposit(self, amount: int) -> bool:
        return amount + self.current_holding <= self.max_capacity
