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
import tempfile
from decimal import Decimal
from unittest.mock import patch

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

    def test_history_records_are_deep_copies(self):
        """Changing a returned transaction cannot alter internal state."""
        acc = BankAccount("Maya", 500.0)
        history = acc.get_transaction_history()
        history[0]["amount"] = Decimal("999999.00")
        self.assertEqual(acc.get_transaction_history()[0]["amount"], Decimal("500.00"))

    def test_non_finite_amount_is_rejected(self):
        """NaN and infinity cannot enter account balances."""
        acc = BankAccount("Nina")
        with self.assertRaises(ValueError):
            acc.deposit("nan")
        with self.assertRaises(ValueError):
            acc.deposit("inf")


class TestSavingsAccount(unittest.TestCase):
    """Tests for SavingsAccount polymorphism and inheritance."""
    
    def test_savings_account_creation(self):
        """SavingsAccount is correctly instantiated with minimum balance constraints."""
        from src.models.bank_account import SavingsAccount
        sa = SavingsAccount("Test user", 1000.0, minimum_balance=200.0)
        self.assertEqual(sa.minimum_balance, 200.0)
        self.assertEqual(sa.balance, 1000.0)
        
    def test_savings_account_valid_withdrawal(self):
        """Withdrawal works perfectly provided minimum balance is maintained."""
        from src.models.bank_account import SavingsAccount
        sa = SavingsAccount("Test user", 1000.0, minimum_balance=200.0)
        sa.withdraw(700.0)
        self.assertEqual(sa.balance, 300.0)
        
    def test_savings_account_insufficient_minimum_balance(self):
        """Polymorphic withdraw() refuses to dip below minimum_balance."""
        from src.models.bank_account import SavingsAccount
        sa = SavingsAccount("Test user", 1000.0, minimum_balance=200.0)
        
        with self.assertRaises(ValueError) as ctx:
            sa.withdraw(900.0)
            
        self.assertIn("Must maintain minimum balance of ₹200.00", str(ctx.exception))
        self.assertEqual(sa.balance, 1000.0)

    def test_savings_account_rejects_opening_balance_below_minimum(self):
        from src.models.bank_account import SavingsAccount
        with self.assertRaises(ValueError):
            SavingsAccount("Test user", 100.0, minimum_balance=200.0)


class TestGlobalReport(unittest.TestCase):
    """Tests for the global customer transaction report."""

    def test_global_report_contains_customer_transaction_details(self):
        from src.main import get_global_report
        from src.models.bank_account import BankAccount

        acc = BankAccount("Alice", 1000.0)
        acc.deposit(250.0)

        rows = get_global_report([acc])
        self.assertEqual(rows[0]["AccountHolder"], "Alice")
        self.assertEqual(rows[0]["TransactionType"], "initial deposit")
        self.assertEqual(rows[1]["TransactionType"], "deposit")
        self.assertEqual(rows[1]["Amount"], 250.0)
        self.assertIn("AccountNumber", rows[0])


class TestCustomerCsvExport(unittest.TestCase):
    """Tests for exporting each customer's details to a CSV file."""

    def test_save_customer_csv_creates_file_with_metadata(self):
        import csv
        import os
        import tempfile

        from src.main import save_customer_csv
        from src.models.bank_account import BankAccount

        acc = BankAccount("Charlie", 2000.0, customer_id=101)
        acc.deposit(300.0)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = save_customer_csv(acc, 28, "Male", "current", temp_dir)
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, newline="") as f:
                rows = list(csv.reader(f))
            self.assertTrue(len(rows) >= 3)
            self.assertEqual(rows[0][0], "CustomerID")
            self.assertEqual(rows[1][1], "Charlie")


class TestCustomerPersistence(unittest.TestCase):
    """Tests for restoring live customer data across application runs."""

    def test_savings_account_round_trip_preserves_rules(self):
        from src.main import load_master_customer_csv, save_master_customer_csv
        from src.models.bank_account import SavingsAccount

        account = SavingsAccount("Olivia", 1000.0, minimum_balance=250.0, customer_id=700)
        account.account_type = "saving"
        account.age = 35
        account.gender = "Female"
        with tempfile.TemporaryDirectory() as temp_dir:
            save_master_customer_csv([account], temp_dir)
            loaded = load_master_customer_csv(os.path.join(temp_dir, "master_customer_report.csv"))

        self.assertEqual(len(loaded), 1)
        self.assertIsInstance(loaded[0], SavingsAccount)
        self.assertEqual(loaded[0].minimum_balance, Decimal("250.00"))
        self.assertEqual(loaded[0].get_balance(), Decimal("1000.00"))

    def test_duplicate_account_numbers_are_rejected(self):
        from src.main import load_master_customer_csv

        contents = (
            "CustomerID,Name,Age,Gender,AccountType,MinimumBalance,AccountNumber,Balance,TransactionID,TransactionType,Amount,Date\n"
            "1,A,30,F,current,,ACC9000,0,,,,\n"
            "2,B,31,M,current,,ACC9000,0,,,,\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", newline="", delete=False) as temp_file:
            temp_file.write(contents)
            file_path = temp_file.name
        try:
            with self.assertRaises(ValueError):
                load_master_customer_csv(file_path)
        finally:
            os.remove(file_path)


class TestExistingAccountOperations(unittest.TestCase):
    """Tests that the operation menu can work with a previously loaded account."""

    def test_existing_account_can_receive_deposit(self):
        from src.main import perform_operations
        account = BankAccount("Peter", 100.0, customer_id=800)
        account.account_type = "current"
        with patch("src.main.ask_for_operation", side_effect=["deposit", "exit"]), \
                patch("src.main.ask_for_amount", return_value=Decimal("25.00")), \
                patch("src.main.save_master_customer_csv"), \
                patch("src.main.TransactionLogger"):
            should_continue = perform_operations(account, [account])

        self.assertFalse(should_continue)
        self.assertEqual(account.get_balance(), Decimal("125.00"))


if __name__ == "__main__":
    unittest.main()
