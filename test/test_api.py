import pytest

from atm.atm import ATM

from dummy import *


def load_atm():
    return ATM(DummyCardReader(), DummyBank())


def load_atm_money_bin():
    return ATM(DummyCardReader(), DummyBank(), money_bin=DummyMoneyBin())


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


def test_get_balance():
    atm = load_atm()
    assert atm.get_balance() == -1
    atm.insert_card()
    assert atm.get_balance() == -1
    atm.validate_pin('1234')
    assert atm.select_account('0001') == 0
    assert atm.get_account_id() == '0001'
    assert atm.get_balance() == 1000

    assert atm.select_account('0002') == 0
    assert atm.get_balance() == 500


def test_deposit():
    atm = load_atm()
    amount = 500
    assert atm.deposit(amount) == -1
    atm.insert_card()
    assert atm.deposit(amount) == -1
    atm.validate_pin('1234')
    assert atm.select_account('0001') == 0
    assert atm.get_account_id() == '0001'
    assert atm.get_balance() == 1000
    assert atm.deposit(amount) == 0
    assert atm.get_balance() == 1000 + amount
    assert atm.deposit(-10) == -5
    assert atm.get_balance() == 1000 + amount


def test_deposit_with_money_bin():
    atm = load_atm_money_bin()
    amount = 500
    assert atm.deposit(amount) == -1
    atm.insert_card()
    assert atm.deposit(amount) == -1
    atm.validate_pin('1234')
    assert atm.select_account('0001') == 0
    assert atm.get_account_id() == '0001'
    assert atm.get_balance() == 1000
    assert atm.deposit(2000) == -2
    assert atm.deposit(amount) == 0
    assert atm.get_balance() == 1000 + amount
    assert atm.deposit(-10) == -5
    assert atm.get_balance() == 1000 + amount


