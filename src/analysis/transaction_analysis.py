"""
transaction_analysis.py

Module for analyzing banking transactions using pandas and NumPy.
DataGrokr PLP Week 2 Mini-Project | Phase 3
"""

import pandas as pd
import numpy as np


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing CSV file: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Data format error in CSV file: {file_path}")


def inspect_data(df: pd.DataFrame) -> dict:
    """
    Return basic inspection data of the DataFrame: shape, and columns.
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist()
    }


def filter_by_type(df: pd.DataFrame, txn_type: str) -> pd.DataFrame:
    """
    Filter the transactions to include only the specified type (e.g., 'Deposit').
    """
    if "TransactionType" not in df.columns:
        raise ValueError("DataFrame missing 'TransactionType' column.")
    
    return df[df["TransactionType"].str.lower() == txn_type.lower()]


def filter_above_amount(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Filter transactions strictly above the given threshold.
    """
    if "Amount" not in df.columns:
        raise ValueError("DataFrame missing 'Amount' column.")
        
    return df[df["Amount"] > threshold]


def group_by_account(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group transactions by AccountNumber to get transaction count and total amount.
    """
    if "AccountNumber" not in df.columns or "Amount" not in df.columns:
        raise ValueError("DataFrame missing required columns for groupby.")
        
    # Group by account and apply aggregation: count and sum
    grouped = df.groupby("AccountNumber").agg({
        "TransactionID": "count",
        "Amount": "sum"
    }).rename(columns={"TransactionID": "TransactionCount", "Amount": "TotalAmount"})
    
    return grouped


def merge_with_accounts(txn_df: pd.DataFrame, acc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge transaction data with account data on 'AccountNumber'.
    """
    # perform an inner join by default
    merged = pd.merge(txn_df, acc_df, on="AccountNumber", how="inner")
    return merged


def numpy_summary(df: pd.DataFrame) -> dict:
    """
    Perform numerical analysis on the 'Amount' column using NumPy.
    """
    if "Amount" not in df.columns:
        raise ValueError("DataFrame missing 'Amount' column.")
        
    # Extract as numpy array
    amounts = df["Amount"].to_numpy()
    
    if len(amounts) == 0:
        return {
            "total": 0.0,
            "mean": 0.0,
            "max": 0.0,
            "min": 0.0
        }
    
    return {
        "total": float(np.sum(amounts)),
        "mean": float(np.mean(amounts)),
        "max": float(np.max(amounts)),
        "min": float(np.min(amounts))
    }


def analyze_transactions(txn_path: str, acc_path: str) -> dict:
    """
    End-to-end analysis method. 
    Loads files, filters, groups, merges, and calculates numpy summaries.
    Returns a unified dictionary of results.
    """
    # 1. Load Data
    txn_df = load_csv(txn_path)
    acc_df = load_csv(acc_path)
    
    # 2. Basic Inspection
    inspection = inspect_data(txn_df)
    
    # 3. Filtering
    deposits_df = filter_by_type(txn_df, "Deposit")
    withdrawals_df = filter_by_type(txn_df, "Withdrawal")
    
    # 4. Groupby
    account_summary = group_by_account(txn_df)
    
    # 5. Merge
    merged_df = merge_with_accounts(txn_df, acc_df)
    
    # 6. NumPy Basic Analysis
    overall_summary = numpy_summary(txn_df)
    
    # Pack up the results
    return {
        "inspection": inspection,
        "total_rows": len(txn_df),
        "total_deposits": len(deposits_df),
        "total_withdrawals": len(withdrawals_df),
        "overall_summary": overall_summary,
        "account_summary_df": account_summary,
        "merged_sample_df": merged_df.head(3) # Return top 3 of merge for display
    }
