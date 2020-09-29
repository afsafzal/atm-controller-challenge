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


def test_release():
    atm = load_atm()
    res = atm.release_card()
    assert res == None

    atm.insert_card()
    res = atm.release_card()
    assert res.number == CARD1.number
    assert not atm.get_card_number()


def test_validate_pin():
    atm = load_atm()
    assert atm.validate_pin('1234') == -1
    atm.insert_card()
    assert atm.validate_pin('8888') == -3
    assert atm.validate_pin('1234') == 0
    assert atm.validate_pin('1234') == -2

    atm.release_card()
    assert atm.validate_pin('1234') == -1
    atm.insert_card()
    assert atm.validate_pin('1234') == 0


def test_get_all_accounts():
    atm = load_atm()
    assert atm.get_all_accounts() == []
    atm.insert_card()
    assert atm.get_all_accounts() == []
    atm.validate_pin('1234')
    assert atm.get_all_accounts() == USER1.accounts


def test_select_account():
    atm = load_atm()
    assert atm.select_account('0001') == -1
    atm.insert_card()
    assert atm.select_account('0001') == -1
    atm.validate_pin('1234')
    assert atm.select_account('0003') == -2
    assert atm.select_account('0001') == 0
    assert atm.get_account_id() == '0001'
    assert atm.select_account('0002') == 0
    assert atm.get_account_id() == '0002'

