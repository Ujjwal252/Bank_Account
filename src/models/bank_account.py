"""
bank_account.py

BankAccount class — core OOP model for the Bank Account Management System.
DataGrokr PLP Week 2 Mini-Project | Phase 2
"""


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

    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        """
        Initialize a new BankAccount.

        Args:
            account_holder (str): Name of the account holder.
            initial_balance (float): Starting balance. Defaults to 0.0.

        Raises:
            ValueError: If initial_balance is negative.
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        # Increment the class counter and assign a formatted account number.
        BankAccount._account_counter += 1
        self.account_number: str = f"ACC{BankAccount._account_counter}"

        self.account_holder: str = account_holder
        self.balance: float = initial_balance

        # Transaction history — list of dicts, one per successful transaction.
        self._transactions: list = []

        # Record opening balance as the first entry if non-zero.
        if initial_balance > 0:
            self._transactions.append({
                "type": "initial deposit",
                "amount": initial_balance,
                "balance": self.balance,
            })

    # ------------------------------------------------------------------ #
    # Deposit
    # ------------------------------------------------------------------ #

    def deposit(self, amount: float) -> None:
        """
        Deposit money into the account.

        Args:
            amount (float): Amount to deposit. Must be greater than zero.

        Raises:
            ValueError: If amount is zero or negative.
        """
        if amount <= 0:
            raise ValueError(f"Deposit amount must be greater than zero. Got: {amount}")

        self.balance += amount
        self._transactions.append({
            "type": "deposit",
            "amount": amount,
            "balance": self.balance,
        })

    # ------------------------------------------------------------------ #
    # Withdraw
    # ------------------------------------------------------------------ #

    def withdraw(self, amount: float) -> None:
        """
        Withdraw money from the account.

        Args:
            amount (float): Amount to withdraw. Must be greater than zero and
                            not exceed the current balance.

        Raises:
            ValueError: If amount is zero or negative.
            ValueError: If amount exceeds the current balance.
        """
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be greater than zero. Got: {amount}")

        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self.balance -= amount
        self._transactions.append({
            "type": "withdrawal",
            "amount": amount,
            "balance": self.balance,
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
        return list(self._transactions)

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
