"""
test_transaction_analysis.py

Unit tests for the pandas transaction analysis module.
DataGrokr PLP Week 2 Mini-Project | Phase 3
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analysis.transaction_analysis import (
    load_csv, inspect_data, filter_by_type, 
    filter_above_amount, group_by_account, 
    merge_with_accounts, numpy_summary
)


class TestTransactionAnalysis(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Find the real CSVs to use for testing against genuine data."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.txn_path = os.path.join(base_dir, "data", "transactions.csv")
        cls.acc_path = os.path.join(base_dir, "data", "accounts.csv")
    
    def setUp(self):
        self.txn_df = load_csv(self.txn_path)
        self.acc_df = load_csv(self.acc_path)

    def test_load_csv_valid(self):
        """Valid CSV loads into DataFrame with expected rows."""
        self.assertIsInstance(self.txn_df, pd.DataFrame)
        self.assertTrue(len(self.txn_df) > 0)
        
    def test_load_csv_invalid_path(self):
        """Invalid CSV path raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_csv("nonexistent_fake_path.csv")

    def test_inspect_data(self):
        """Inspection returns shape and columns."""
        res = inspect_data(self.txn_df)
        self.assertIn("shape", res)
        self.assertIn("columns", res)
        self.assertEqual(res["columns"], ["TransactionID", "AccountNumber", "AccountHolder", "TransactionType", "Amount", "Date"])
        
    def test_filter_by_type(self):
        """Filtering by Deposit returns only Deposits."""
        deposits = filter_by_type(self.txn_df, "Deposit")
        unique_types = deposits["TransactionType"].unique()
        self.assertEqual(len(unique_types), 1)
        self.assertEqual(unique_types[0], "Deposit")

    def test_filter_above_amount(self):
        """Filtering amount > threshold works reliably."""
        threshold = 3000.0
        large_txns = filter_above_amount(self.txn_df, threshold)
        self.assertTrue((large_txns["Amount"] > threshold).all())

    def test_group_by_account(self):
        """Groupby AccountNumber computes count and total Amount."""
        grouped = group_by_account(self.txn_df)
        self.assertIn("TransactionCount", grouped.columns)
        self.assertIn("TotalAmount", grouped.columns)
        # Check one specific account sum, e.g., ACC1001 amounts to 5000+2000-1500-800+3000 ? Wait, amount is purely absolute.
        # So sum of all transactions for ACC1001 = 5000+2000+1500+800+3000 = 12300
        self.assertEqual(grouped.loc["ACC1001", "TotalAmount"], 12300.0)

    def test_merge_with_accounts(self):
        """Merging transactions with accounts joins on AccountNumber."""
        merged = merge_with_accounts(self.txn_df, self.acc_df)
        # Should include columns from both: TransactionID, AccountType, Branch, etc.
        self.assertIn("TransactionID", merged.columns)
        self.assertIn("AccountType", merged.columns)
        # Row count should be same as txn_df if all txn accounts exist in acc_df
        self.assertEqual(len(merged), len(self.txn_df))

    def test_numpy_summary(self):
        """NumPy aggregates max, min, mean, sum correctly."""
        summary = numpy_summary(self.txn_df)
        self.assertIn("total", summary)
        self.assertIn("max", summary)
        self.assertIn("min", summary)
        
        amounts = self.txn_df["Amount"].to_numpy()
        self.assertEqual(summary["total"], np.sum(amounts))
        self.assertEqual(summary["max"], np.max(amounts))


if __name__ == "__main__":
    unittest.main()
