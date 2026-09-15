"""
main.py

Run from project root:
    python run.py
"""

import csv
import os
import tempfile
from decimal import Decimal
from pathlib import Path
from src.models.bank_account import BankAccount, SavingsAccount
from src.services.transaction_logger import TransactionLogger


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MASTER_REPORT_PATH = PROJECT_ROOT / "data" / "master_customer_report.csv"
TRANSACTION_LOG_PATH = PROJECT_ROOT / "data" / "app_transaction_log.txt"


def print_transaction_history(account: BankAccount) -> None:
    """Print all transactions for the given account with a timestamp."""
    history = account.get_transaction_history()

    if not history:
        print("  No transactions yet.")
        return

    print(f"  {'#':<4} {'Type':<18} {'Amount':>10} {'Balance':>12} {'Date & Time':>20}")
    print("  " + "-" * 80)
    for i, txn in enumerate(history, start=1):
        timestamp = txn.get("timestamp", "N/A")
        print(
            f"  {i:<4} {txn['type']:<18} "
            f"{'₹{:.2f}'.format(txn['amount']):>10} "
            f"{'₹{:.2f}'.format(txn['balance']):>12} "
            f"{timestamp:>20}"
        )


def show_all_accounts(accounts: list[BankAccount]) -> None:
    """Display all created accounts with balance and transaction history."""
    if not accounts:
        print("No accounts available yet.")
        return

    print("\nAll customer accounts")
    print("=" * 120)
    for account in accounts:
        print(f"Customer ID: {account.customer_id} | Name: {account.account_holder} | Account Number: {account.account_number} | Balance: ₹{account.get_balance():.2f}")
        print_transaction_history(account)
        print()
    print("=" * 120)


def get_global_report(accounts: list[BankAccount]) -> list[dict]:
    """Return all transaction records from all accounts in a uniform report format."""
    rows = []

    for account in accounts:
        history = account.get_transaction_history()
        for index, txn in enumerate(history, start=1):
            rows.append({
                "TransactionID": f"{account.account_number}-{index}",
                "AccountNumber": account.account_number,
                "AccountHolder": account.account_holder,
                "TransactionType": txn.get("type", "N/A"),
                "Amount": txn.get("amount", 0.0),
                "Date": txn.get("timestamp", "N/A"),
            })

    return rows


def print_global_report(accounts: list[BankAccount]) -> None:
    """Print a global report of all transactions from all customers."""
    rows = get_global_report(accounts)

    if not rows:
        print("No customer records are available yet.")
        return

    print("\nGlobal customer report")
    print("=" * 150)
    print(f"{'TransactionID':<18} {'AccountNumber':<15} {'AccountHolder':<22} {'TransactionType':<18} {'Amount':>12} {'Date':>20}")
    print("-" * 150)
    for row in rows:
        print(
            f"{row['TransactionID']:<18} "
            f"{row['AccountNumber']:<15} "
            f"{row['AccountHolder']:<22} "
            f"{row['TransactionType']:<18} "
            f"₹{row['Amount']:>10.2f} "
            f"{row['Date']:>20}"
        )
    print("=" * 150)


def load_master_customer_csv(file_path: str | os.PathLike = MASTER_REPORT_PATH) -> list[BankAccount]:
    """Load customer records from the master CSV file into memory."""
    if not os.path.exists(file_path):
        return []

    accounts_by_id: dict[int, BankAccount] = {}
    account_numbers: set[str] = set()
    highest_account_number = BankAccount._account_counter

    with open(file_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row or not row.get("CustomerID"):
                continue

            try:
                customer_id = int(row["CustomerID"])
            except (TypeError, ValueError):
                raise ValueError("Invalid customer ID in master customer report.") from None
            if customer_id <= 0:
                raise ValueError("Customer IDs must be positive.")
            account_number = row.get("AccountNumber", "")
            account_holder = row.get("Name", "")
            age = row.get("Age", "")
            gender = row.get("Gender", "")
            account_type = (row.get("AccountType") or "current").strip().lower()
            minimum_balance = row.get("MinimumBalance", "")

            if age:
                try:
                    age_value = int(age)
                except ValueError:
                    raise ValueError(f"Invalid age for customer {customer_id}.") from None
                if not 1 <= age_value <= 120:
                    raise ValueError(f"Age for customer {customer_id} must be between 1 and 120.")
            else:
                age_value = None

            if account_number and account_number in account_numbers and customer_id not in accounts_by_id:
                raise ValueError(f"Duplicate account number in master report: {account_number}")

            if customer_id not in accounts_by_id:
                if account_type == "saving":
                    try:
                        saved_minimum = BankAccount._to_money(minimum_balance or "500.00", "Minimum balance")
                    except ValueError as error:
                        raise ValueError(f"Invalid minimum balance for customer {customer_id}: {error}") from None
                    account = SavingsAccount(
                        account_holder,
                        initial_balance=saved_minimum,
                        minimum_balance=saved_minimum,
                        customer_id=customer_id,
                    )
                    account.balance = Decimal("0.00")
                    account._transactions.clear()
                else:
                    account = BankAccount(account_holder, initial_balance=0.0, customer_id=customer_id)
                account.age = age_value
                account.gender = gender
                account.account_type = account_type
                account.account_number = account_number or account.account_number
                accounts_by_id[customer_id] = account
                if account_number:
                    account_numbers.add(account_number)

                if account_number.startswith("ACC"):
                    try:
                        highest_account_number = max(
                            highest_account_number,
                            int(account_number[3:]),
                        )
                    except ValueError:
                        pass

            account = accounts_by_id[customer_id]
            txn_type = row.get("TransactionType", "").strip()
            amount = row.get("Amount", "")
            timestamp = row.get("Date", "")

            if txn_type:
                try:
                    amount_value = BankAccount._to_money(amount or "0.00", "Transaction amount")
                except ValueError as error:
                    raise ValueError(f"Invalid transaction for customer {customer_id}: {error}") from None

                current_balance = account.get_balance()
                if txn_type.lower() == "deposit":
                    current_balance += amount_value
                elif txn_type.lower() == "withdrawal":
                    current_balance -= amount_value
                elif txn_type.lower() == "initial deposit":
                    current_balance += amount_value

                if txn_type.lower() not in {"deposit", "withdrawal", "initial deposit"}:
                    raise ValueError(f"Unknown transaction type: {txn_type}")

                account.balance = current_balance
                account._transactions.append({
                    "type": txn_type,
                    "amount": amount_value,
                    "balance": current_balance,
                    "timestamp": timestamp,
                })

    BankAccount._account_counter = highest_account_number
    return list(accounts_by_id.values())


def save_master_customer_csv(customers: list[BankAccount], folder: str | os.PathLike | None = None) -> str:
    """Write all customers and their transactions into one master CSV file."""
    folder_path = Path(folder) if folder is not None else MASTER_REPORT_PATH.parent
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / "master_customer_report.csv"

    fieldnames = [
        "CustomerID",
        "Name",
        "Age",
        "Gender",
        "AccountType",
        "MinimumBalance",
        "AccountNumber",
        "Balance",
        "TransactionID",
        "TransactionType",
        "Amount",
        "Date",
    ]

    rows = []
    for account in customers:
        history = account.get_transaction_history()
        age_value = getattr(account, "age", "")
        gender_value = getattr(account, "gender", "")
        account_type_value = getattr(account, "account_type", "current")
        minimum_balance_value = getattr(account, "minimum_balance", "")

        if not history:
            rows.append({
                "CustomerID": account.customer_id,
                "Name": account.account_holder,
                "Age": age_value,
                "Gender": gender_value,
                "AccountType": account_type_value,
                "MinimumBalance": minimum_balance_value,
                "AccountNumber": account.account_number,
                "Balance": account.get_balance(),
                "TransactionID": "",
                "TransactionType": "",
                "Amount": "",
                "Date": "",
            })
            continue

        for index, txn in enumerate(history, start=1):
            rows.append({
                "CustomerID": account.customer_id,
                "Name": account.account_holder,
                "Age": age_value,
                "Gender": gender_value,
                "AccountType": account_type_value,
                "MinimumBalance": minimum_balance_value,
                "AccountNumber": account.account_number,
                "Balance": account.get_balance(),
                "TransactionID": f"{account.account_number}-{index}",
                "TransactionType": txn.get("type", "N/A"),
                "Amount": txn.get("amount", 0.0),
                "Date": txn.get("timestamp", "N/A"),
            })

    with tempfile.NamedTemporaryFile(
        mode="w",
        newline="",
        encoding="utf-8",
        dir=folder_path,
        prefix="master_customer_report_",
        suffix=".tmp",
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
        writer = csv.DictWriter(temporary_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    try:
        os.replace(temporary_path, file_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise

    print(f"Master customer report saved to: {file_path}")
    return str(file_path)


def save_customer_csv(account: BankAccount, age: int, gender: str, account_type: str, folder: str = "data") -> str:
    """Backward-compatible wrapper that writes to the master customer CSV file."""
    account.age = age
    account.gender = gender
    account.account_type = account_type.strip().lower()
    customers = [account]
    return save_master_customer_csv(customers, folder=folder)


def ask_for_text(prompt: str, field_name: str) -> str:
    """Ask the user for a non-empty text value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty. Please try again.")


def ask_for_int(prompt: str, field_name: str) -> int:
    """Ask the user for a valid integer value."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print(f"Please enter a valid number for {field_name}.")
            continue
        if field_name == "customer ID" and value <= 0:
            print("Customer ID must be positive.")
            continue
        if field_name == "customer age" and not 1 <= value <= 120:
            print("Customer age must be between 1 and 120.")
            continue
        return value


def ask_for_amount(prompt: str, *, allow_zero: bool = False) -> Decimal:
    """Ask the user for a valid monetary amount."""
    while True:
        try:
            value = BankAccount._to_money(input(prompt).strip())
        except ValueError:
            print("Please enter a valid amount. Example: 1000 or 2500.50")
            continue

        if value < 0:
            print("Amount cannot be negative.")
            continue

        if not allow_zero and value == 0:
            print("Amount must be greater than zero.")
            continue

        return value


def choose_account_type() -> str:
    """Ask the user to choose current or saving account."""
    while True:
        account_type = input("Enter account type (current / saving): ").strip().lower()
        if account_type in {"current", "saving"}:
            return account_type
        print("Invalid account type. Please enter either 'current' or 'saving'.")


def ask_for_operation() -> str:
    """Ask the user to choose a banking operation by number or name."""
    while True:
        print("\n1. Deposit\n2. Withdraw\n3. Check balance\n4. View account\n5. Transaction history\n6. All accounts\n7. Analytics report\n8. Exit")
        operation = input("Choose an option: ").strip().lower()
        operation = {
            "1": "deposit",
            "2": "withdraw",
            "3": "check balance",
            "4": "view account",
            "5": "transaction history",
            "6": "all accounts",
            "7": "analytics report",
            "8": "exit",
        }.get(operation, operation)

        valid_ops = {
            "deposit",
            "withdraw",
            "check balance",
            "balance",
            "view account",
            "account details",
            "transaction history",
            "history",
            "all accounts",
            "accounts",
            "analytics report",
            "analytics",
            "exit",
            "quit",
        }

        if operation in valid_ops:
            return operation

        print("Invalid operation. Please choose one of the listed options.")


def create_customer_account(customers: list[BankAccount], used_customer_ids: set[int]) -> BankAccount:
    """Create a single customer account from prompt input."""
    customer_id = ask_for_int("Enter customer ID: ", "customer ID")
    while customer_id in used_customer_ids:
        print("This customer ID is already in use. Please enter a unique ID.")
        customer_id = ask_for_int("Enter customer ID: ", "customer ID")
    used_customer_ids.add(customer_id)

    customer_name = ask_for_text("Enter customer name: ", "Customer name")
    customer_age = ask_for_int("Enter customer age: ", "customer age")
    customer_gender = ask_for_text("Enter customer gender: ", "Gender")
    account_type = choose_account_type()
    opening_balance = ask_for_amount("Enter opening balance: ₹")

    minimum_balance = Decimal("0.00")
    if account_type == "saving":
        minimum_balance = ask_for_amount(
            "Enter minimum balance required for saving account: ₹",
            allow_zero=True,
        )
        while opening_balance < minimum_balance:
            print("Opening balance must be at least the required minimum balance.")
            opening_balance = ask_for_amount("Enter opening balance: ₹")

    if account_type == "saving":
        account = SavingsAccount(
            customer_name,
            initial_balance=opening_balance,
            minimum_balance=minimum_balance,
            customer_id=customer_id,
        )
        account.age = customer_age
        account.gender = customer_gender
        account.account_type = "saving"
        print(f"\nSavings account created successfully for {customer_name}.")
    else:
        account = BankAccount(customer_name, initial_balance=opening_balance, customer_id=customer_id)
        account.age = customer_age
        account.gender = customer_gender
        account.account_type = "current"
        print(f"\nCurrent account created successfully for {customer_name}.")

    customers.append(account)
    print(f"Generated Account Number: {account.account_number}")
    print(f"Customer ID: {account.customer_id}")
    print(f"Age: {customer_age}")
    print(f"Gender: {customer_gender}")
    print(f"Account Type: {account_type.title()}")
    print(f"Current Balance: ₹{account.get_balance():.2f}")

    save_master_customer_csv(customers)
    return account


def choose_existing_account(customers: list[BankAccount]) -> BankAccount | None:
    """Select an existing account by customer ID or account number."""
    if not customers:
        print("No customer accounts are available yet.")
        return None

    show_all_accounts(customers)
    selected = input("Enter customer ID or account number: ").strip().lower()
    for account in customers:
        if selected in {str(account.customer_id).lower(), account.account_number.lower()}:
            return account
    print("No account matched that customer ID or account number.")
    return None


def print_live_analytics(accounts: list[BankAccount]) -> None:
    """Print useful analytics calculated from live customer records."""
    rows = get_global_report(accounts)
    deposits = [row["Amount"] for row in rows if row["TransactionType"].lower() in {"deposit", "initial deposit"}]
    withdrawals = [row["Amount"] for row in rows if row["TransactionType"].lower() == "withdrawal"]
    total_deposits = sum(deposits, Decimal("0.00"))
    total_withdrawals = sum(withdrawals, Decimal("0.00"))
    combined_balance = sum((account.get_balance() for account in accounts), Decimal("0.00"))
    print("\nLive analytics report")
    print("=" * 45)
    print(f"Customers: {len(accounts)}")
    print(f"Transactions: {len(rows)}")
    print(f"Total deposits: ₹{total_deposits:.2f}")
    print(f"Total withdrawals: ₹{total_withdrawals:.2f}")
    print(f"Net movement: ₹{total_deposits - total_withdrawals:.2f}")
    print(f"Current combined balance: ₹{combined_balance:.2f}")


def perform_operations(account: BankAccount, customers: list[BankAccount]) -> bool:
    """Run the operation menu for an account; return False when the app should exit."""
    while True:
        operation = ask_for_operation()
        if operation in {"exit", "quit"}:
            return False
        if operation in {"check balance", "balance"}:
            print(f"Available balance: ₹{account.get_balance():.2f}")
            continue
        if operation in {"view account", "account details"}:
            account.display_account()
            continue
        if operation in {"transaction history", "history"}:
            print_transaction_history(account)
            continue
        if operation in {"all accounts", "accounts"}:
            show_all_accounts(customers)
            continue
        if operation in {"analytics report", "analytics"}:
            print_live_analytics(customers)
            continue

        amount = ask_for_amount("Enter amount: ₹")
        try:
            if operation == "deposit":
                account.deposit(amount)
                message = f"Deposit of ₹{amount:.2f}"
            else:
                account.withdraw(amount)
                message = f"Withdrawal of ₹{amount:.2f}"
            save_master_customer_csv(customers)
            with TransactionLogger(TRANSACTION_LOG_PATH) as logger:
                logger.log(f"{message} | Account: {account.account_number} | Balance: ₹{account.get_balance():.2f}")
            print(f"{message} was successful.")
            print(f"Updated balance: ₹{account.get_balance():.2f}")
        except ValueError as error:
            print(f"Operation failed: {error}")


def main() -> None:
    print("=" * 70)
    print("Welcome to the Bank Account Management System")
    print("=" * 70)

    customers = load_master_customer_csv()
    used_customer_ids = {account.customer_id for account in customers if account.customer_id is not None}

    while True:
        choice = input(
            "\nChoose an action: add customer, view customers, analytics, or exit: "
        ).strip().lower()

        if choice in {"exit", "quit"}:
            print("Thank you for banking with us. Goodbye!")
            break

        if choice in {"view", "old", "details", "report"}:
            if not customers:
                print("There are no old customer records available yet.")
            else:
                print_global_report(customers)
                show_all_accounts(customers)
                selected_account = choose_existing_account(customers)
                if selected_account is not None and not perform_operations(selected_account, customers):
                    print("Thank you for banking with us. Goodbye!")
                    break
            continue

        if choice in {"analytics", "analytics report"}:
            print_live_analytics(customers)
            continue

        if choice in {"add", "new"}:
            account = create_customer_account(customers, used_customer_ids)
            if not perform_operations(account, customers):
                print("Thank you for banking with us. Goodbye!")
                break
            continue

        print("Invalid choice. Please enter add, view, analytics, or exit.")


if __name__ == "__main__":
    main()
