"""
decorators.py

Custom decorators for the Bank Account Management System.
DataGrokr PLP Week 2 Mini-Project | Phase 4
"""

from functools import wraps


def log_transaction(func):
    """
    Decorator that logs the execution of a bank account transaction.
    
    It prints a message before the transaction starts, and upon success.
    If the transaction fails with an Exception (like ValueError for invalid amounts),
    it logs the failure and re-raises the exception.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract amount if it was passed via args or kwargs. 
        # Typically for deposit(self, amount) or withdraw(self, amount), 
        # amount is args[1] or kwargs['amount']
        amount = None
        if len(args) > 1:
            amount = args[1]
        elif 'amount' in kwargs:
            amount = kwargs['amount']
            
        operation_name = func.__name__
        amount_str = f" amount={amount}" if amount is not None else ""
        
        print(f"  [LOG] {operation_name} called with{amount_str}")
        
        try:
            result = func(*args, **kwargs)
            print(f"  [LOG] {operation_name} completed successfully")
            return result
        except Exception as e:
            print(f"  [LOG] {operation_name} failed: {e.__class__.__name__} - {e}")
            raise
            
    return wrapper
