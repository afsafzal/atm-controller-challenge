import pytest

from atm.atm import ATM

from dummy import *


def load_atm():
    return ATM(DummyCardReader(), DummyBank())



def test_insert():
    atm = load_atm()
    res = atm.insert_card()
    assert res == 0
    assert atm.get_card_number() == CARD1.number
    res = atm.insert_card()
    assert res == -1
    assert atm.get_card_number() == CARD1.number

    atm = ATM(BadCardReader(), DummyBank())
    res = atm.insert_card()
    assert res == -2
    assert not atm.get_card_number()
