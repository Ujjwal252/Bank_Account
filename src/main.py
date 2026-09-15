"""
main.py

CLI demonstration of the BankAccount class and pandas Analysis.
DataGrokr PLP Week 2 Mini-Project | Phase 2 & 3

Run from project root:
    python run.py
"""

import os
from src.models.bank_account import BankAccount
from src.analysis.transaction_analysis import analyze_transactions


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
    print("   BANK ACCOUNT MANAGEMENT (PART A)")
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

    # ── 5. Display transaction history ────────────────────────────────
    print("\n[4] Transaction History:")
    print_transaction_history(account)

    print("\n\n" + "=" * 50)
    print("   TRANSACTION DATA ANALYSIS (PART B)")
    print("=" * 50)
    
    # Define absolute paths dynamically based on current location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txn_path = os.path.join(base_dir, "data", "transactions.csv")
    acc_path = os.path.join(base_dir, "data", "accounts.csv")
    
    try:
        results = analyze_transactions(txn_path, acc_path)
        print("\n✓ CSV loaded successfully.")
        
        print("\n[Data Inspection]")
        print(f"  Shape: {results['inspection']['shape']}")
        print(f"  Columns: {', '.join(results['inspection']['columns'])}")
        
        print("\n[Overall Totals (Filtering)]")
        print(f"  Total transaction rows: {results['total_rows']}")
        print(f"  Total deposits: {results['total_deposits']}")
        print(f"  Total withdrawals: {results['total_withdrawals']}")
        
        print("\n[NumPy Summary (Amounts)]")
        summary = results['overall_summary']
        print(f"  Total amount volume: ₹{summary['total']:.2f}")
        print(f"  Average transaction: ₹{summary['mean']:.2f}")
        print(f"  Max transaction:     ₹{summary['max']:.2f}")
        print(f"  Min transaction:     ₹{summary['min']:.2f}")
        
        print("\n[Group By Account (pandas groupby)]")
        print(results['account_summary_df'].to_string())
        
        print("\n[Merged Account + Transaction info (pandas merge) - Top 3]")
        print(results['merged_sample_df'].to_string(index=False))
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")

    print("\n" + "=" * 50)
    print("   Demo complete.")
    print("=" * 50)


if __name__ == "__main__":
    main()
