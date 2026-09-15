"""
main.py

CLI demonstration of the BankAccount class.
DataGrokr PLP Week 2 Mini-Project | Phase 2

Run from project root:
    python src/main.py
"""

from src.models.bank_account import BankAccount


def print_transaction_history(account: BankAccount) -> None:
    """Print all transactions for the given account."""
    history = account.get_transaction_history()

    if not history:
        print("  No transactions yet.")
        return

    print(f"  {'#':<4} {'Type':<18} {'Amount':>10} {'Balance':>12}")
    print("  " + "-" * 46)
    for i, txn in enumerate(history, start=1):
        print(
            f"  {i:<4} {txn['type']:<18} "
            f"{'₹{:.2f}'.format(txn['amount']):>10} "
            f"{'₹{:.2f}'.format(txn['balance']):>12}"
        )


def main() -> None:
    print("=" * 50)
    print("   Bank Account Management System")
    print("   DataGrokr PLP — Week 2 Demo")
    print("=" * 50)

    # ── 1. Create a new bank account ──────────────────────────────────
    print("\n[1] Creating account for Arjun Sharma with ₹5,000 initial balance...")
    account = BankAccount("Arjun Sharma", 5000.0)
    account.display_account()

    # ── 2. Perform a valid deposit ────────────────────────────────────
    print("\n[2] Depositing ₹2,000...")
    account.deposit(2000.0)
    print(f"    ✓ Deposit successful. New balance: ₹{account.get_balance():.2f}")

    # ── 3. Perform a valid withdrawal ─────────────────────────────────
    print("\n[3] Withdrawing ₹1,500...")
    account.withdraw(1500.0)
    print(f"    ✓ Withdrawal successful. New balance: ₹{account.get_balance():.2f}")

    # ── 4. Display updated account info ───────────────────────────────
    print("\n[4] Updated account details:")
    account.display_account()

    # ── 5. Display transaction history ────────────────────────────────
    print("\n[5] Transaction History:")
    print_transaction_history(account)

    # ── 6. Exception handling — invalid deposit ───────────────────────
    print("\n[6] Attempting invalid deposit of ₹-500...")
    try:
        account.deposit(-500.0)
    except ValueError as e:
        print(f"    ✗ Caught ValueError: {e}")

    # ── 7. Exception handling — insufficient balance ──────────────────
    print("\n[7] Attempting withdrawal of ₹99,999 (exceeds balance)...")
    try:
        account.withdraw(99999.0)
    except ValueError as e:
        print(f"    ✗ Caught ValueError: {e}")

    print(f"\n    Balance unchanged: ₹{account.get_balance():.2f}")

    print("\n" + "=" * 50)
    print("   Demo complete.")
    print("=" * 50)


if __name__ == "__main__":
    main()
