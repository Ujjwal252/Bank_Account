"""
test_bank_account.py

Unit tests for the BankAccount class.
DataGrokr PLP Week 2 Mini-Project | Phase 2

Run with:
    python -m unittest tests/test_bank_account.py   (from project root)
or:
    python -m unittest discover -s tests
"""

import unittest
import sys
import os

# Ensure the project root is on the path so 'src' can be imported.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.bank_account import BankAccount


class TestBankAccountCreation(unittest.TestCase):
    """Tests for account creation and initial state."""

    def test_account_creation_with_initial_balance(self):
        """Account is created with the correct holder name and balance."""
        acc = BankAccount("Alice", 5000.0)
        self.assertEqual(acc.account_holder, "Alice")
        self.assertEqual(acc.get_balance(), 5000.0)

    def test_account_creation_zero_balance(self):
        """Account can be created with a zero initial balance (default)."""
        acc = BankAccount("Bob")
        self.assertEqual(acc.get_balance(), 0.0)

    def test_account_number_is_unique(self):
        """Each account gets a different account number."""
        acc1 = BankAccount("Carol")
        acc2 = BankAccount("Dave")
        self.assertNotEqual(acc1.account_number, acc2.account_number)

    def test_account_number_format(self):
        """Account number starts with 'ACC'."""
        acc = BankAccount("Eve")
        self.assertTrue(acc.account_number.startswith("ACC"))

    def test_negative_initial_balance_raises(self):
        """Creating an account with a negative balance raises ValueError."""
        with self.assertRaises(ValueError):
            BankAccount("Frank", -100.0)


class TestDeposit(unittest.TestCase):
    """Tests for the deposit method."""

    def setUp(self):
        self.acc = BankAccount("Grace", 1000.0)

    def test_valid_deposit_increases_balance(self):
        """A valid deposit increases the balance by the deposited amount."""
        self.acc.deposit(500.0)
        self.assertEqual(self.acc.get_balance(), 1500.0)

    def test_deposit_zero_raises(self):
        """Depositing zero raises a ValueError."""
        with self.assertRaises(ValueError):
            self.acc.deposit(0)

    def test_deposit_negative_raises(self):
        """Depositing a negative amount raises a ValueError."""
        with self.assertRaises(ValueError):
            self.acc.deposit(-200.0)

    def test_invalid_deposit_does_not_change_balance(self):
        """Balance remains unchanged after an invalid deposit attempt."""
        original = self.acc.get_balance()
        try:
            self.acc.deposit(-200.0)
        except ValueError:
            pass
        self.assertEqual(self.acc.get_balance(), original)

    def test_deposit_recorded_in_history(self):
        """A successful deposit is recorded in transaction history."""
        self.acc.deposit(300.0)
        history = self.acc.get_transaction_history()
        # Last entry should be the deposit
        last = history[-1]
        self.assertEqual(last["type"], "deposit")
        self.assertEqual(last["amount"], 300.0)


class TestWithdraw(unittest.TestCase):
    """Tests for the withdraw method."""

    def setUp(self):
        self.acc = BankAccount("Heidi", 2000.0)

    def test_valid_withdrawal_decreases_balance(self):
        """A valid withdrawal reduces the balance correctly."""
        self.acc.withdraw(800.0)
        self.assertEqual(self.acc.get_balance(), 1200.0)

    def test_withdraw_zero_raises(self):
        """Withdrawing zero raises a ValueError."""
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)

    def test_withdraw_negative_raises(self):
        """Withdrawing a negative amount raises a ValueError."""
        with self.assertRaises(ValueError):
            self.acc.withdraw(-100.0)

    def test_insufficient_balance_raises(self):
        """Withdrawing more than the balance raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.acc.withdraw(5000.0)
        self.assertIn("Insufficient balance", str(ctx.exception))

    def test_insufficient_balance_does_not_change_balance(self):
        """Balance stays unchanged when withdrawal exceeds available funds."""
        original = self.acc.get_balance()
        try:
            self.acc.withdraw(5000.0)
        except ValueError:
            pass
        self.assertEqual(self.acc.get_balance(), original)

    def test_withdrawal_recorded_in_history(self):
        """A successful withdrawal is recorded in transaction history."""
        self.acc.withdraw(500.0)
        history = self.acc.get_transaction_history()
        last = history[-1]
        self.assertEqual(last["type"], "withdrawal")
        self.assertEqual(last["amount"], 500.0)


class TestTransactionHistory(unittest.TestCase):
    """Tests for get_transaction_history."""

    def test_initial_transaction_recorded(self):
        """An account opened with funds has one initial transaction."""
        acc = BankAccount("Ivan", 1000.0)
        history = acc.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "initial deposit")

    def test_zero_balance_account_has_empty_history(self):
        """An account opened with zero balance has no transactions."""
        acc = BankAccount("Judy")
        self.assertEqual(len(acc.get_transaction_history()), 0)

    def test_history_grows_with_operations(self):
        """History length increases after each successful operation."""
        acc = BankAccount("Karl", 500.0)  # 1 initial
        acc.deposit(200.0)                # 2
        acc.withdraw(100.0)               # 3
        self.assertEqual(len(acc.get_transaction_history()), 3)

    def test_history_is_a_copy(self):
        """Modifying the returned list does NOT affect internal history."""
        acc = BankAccount("Laura", 500.0)
        history = acc.get_transaction_history()
        history.clear()  # try to wipe it
        # Internal history should still have the initial deposit
        self.assertEqual(len(acc.get_transaction_history()), 1)


if __name__ == "__main__":
    unittest.main()
