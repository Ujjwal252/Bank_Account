"""
bank_account.py

BankAccount class — core OOP model for the Bank Account Management System.
DataGrokr PLP Week 2 Mini-Project | Phase 2 & 4
"""

from copy import deepcopy
from datetime import datetime
from decimal import Decimal, InvalidOperation

from src.services.decorators import log_transaction


class BankAccount:
    """
    Represents a bank account for a single account holder.

    Attributes:
        account_holder (str): Full name of the account holder.
        account_number (str): Unique account identifier (auto-generated).
        balance (float): Current account balance.
        transactions (list): History of all successful transactions.

    Class Attributes:
        _account_counter (int): Shared counter used to generate unique account numbers.
    """

    # Class-level counter — increments each time a new account is created.
    _account_counter = 1000

    def __init__(self, account_holder: str, initial_balance: Decimal | float | str = 0.0, customer_id: int = None):
        """
        Initialize a new BankAccount.

        Args:
            account_holder (str): Name of the account holder.
            initial_balance (float): Starting balance. Defaults to 0.0.
            customer_id (int | None): Unique customer identifier.

        Raises:
            ValueError: If initial_balance is negative.
        """
        if not account_holder or not account_holder.strip():
            raise ValueError("Account holder name cannot be empty.")

        initial_balance = self._to_money(initial_balance, "Initial balance")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        BankAccount._account_counter += 1
        self.account_number: str = f"ACC{BankAccount._account_counter}"
        self.account_holder: str = account_holder
        self.customer_id: int | None = customer_id
        self.balance: Decimal = initial_balance
        self._transactions: list = []

        if initial_balance > 0:
            self._transactions.append({
                "type": "initial deposit",
                "amount": initial_balance,
                "balance": self.balance,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    # ------------------------------------------------------------------ #
    # Deposit
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_money(amount: Decimal | float | str, field_name: str = "Amount") -> Decimal:
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError(f"{field_name} must be a valid number.") from None

        if not value.is_finite():
            raise ValueError(f"{field_name} must be a finite number.")
        return value.quantize(Decimal("0.01"))

    @log_transaction
    def deposit(self, amount: Decimal | float | str) -> None:
        """
        Deposit money into the account.

        Args:
            amount (float): Amount to deposit. Must be greater than zero.

        Raises:
            ValueError: If amount is zero or negative.
        """
        amount = self._to_money(amount, "Deposit amount")
        if amount <= 0:
            raise ValueError(f"Deposit amount must be greater than zero. Got: {amount}")

        self.balance += amount
        self._transactions.append({
            "type": "deposit",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    # ------------------------------------------------------------------ #
    # Withdraw
    # ------------------------------------------------------------------ #

    @log_transaction
    def withdraw(self, amount: Decimal | float | str) -> None:
        """
        Withdraw money from the account.

        Args:
            amount (float): Amount to withdraw. Must be greater than zero and
                            not exceed the current balance.

        Raises:
            ValueError: If amount is zero or negative.
            ValueError: If amount exceeds the current balance.
        """
        amount = self._to_money(amount, "Withdrawal amount")
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be greater than zero. Got: {amount}")

        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self.balance -= amount
        self._transactions.append({
            "type": "withdrawal",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    # ------------------------------------------------------------------ #
    # Balance
    # ------------------------------------------------------------------ #

    def get_balance(self) -> float:
        """
        Return the current account balance.

        Returns:
            float: Current balance.
        """
        return self.balance

    # ------------------------------------------------------------------ #
    # Transaction History
    # ------------------------------------------------------------------ #

    def get_transaction_history(self) -> list:
        """
        Return a copy of the transaction history.

        Returns a copy so the caller cannot accidentally modify
        the internal transaction list.

        Returns:
            list: List of transaction dicts.
        """
        return deepcopy(self._transactions)

    # ------------------------------------------------------------------ #
    # Display
    # ------------------------------------------------------------------ #

    def display_account(self) -> None:
        """Print a summary of the account details to the console."""
        print("-" * 40)
        print("  Account Holder :", self.account_holder)
        print("  Account Number :", self.account_number)
        print("  Balance        : ₹{:.2f}".format(self.balance))
        print("-" * 40)

    # ------------------------------------------------------------------ #
    # String representation
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return (
            f"BankAccount({self.account_holder!r}, "
            f"acc={self.account_number}, "
            f"balance=₹{self.balance:.2f})"
        )


class SavingsAccount(BankAccount):
    """
    Demonstrates Inheritance and Polymorphism.
    A SavingsAccount is a BankAccount that enforces a minimum balance.
    """
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0, minimum_balance: float = 500.0, customer_id: int = None):
        minimum_balance = self._to_money(minimum_balance, "Minimum balance")
        if minimum_balance < 0:
            raise ValueError("Minimum balance cannot be negative.")
        super().__init__(account_holder, initial_balance, customer_id=customer_id)
        if self.balance < minimum_balance:
            raise ValueError("Initial balance cannot be below the minimum balance.")
        self.minimum_balance = minimum_balance
        
    @log_transaction
    def withdraw(self, amount: Decimal | float | str) -> None:
        """
        Polymorphic overridden method.
        Withdraws money but leaves the required minimum balance in the account.
        """
        amount = self._to_money(amount, "Withdrawal amount")
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be greater than zero. Got: {amount}")

        if (self.balance - amount) < self.minimum_balance:
            raise ValueError(f"Insufficient balance. Must maintain minimum balance of ₹{self.minimum_balance:.2f}.")

        self.balance -= amount
        self._transactions.append({
            "type": "withdrawal",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        
    def __str__(self) -> str:
        return (
            f"SavingsAccount({self.account_holder!r}, "
            f"acc={self.account_number}, "
            f"balance=₹{self.balance:.2f}, "
            f"min=₹{self.minimum_balance:.2f})"
        )
