"""
transaction_logger.py

Context manager for writing transaction logs to a file securely.
DataGrokr PLP Week 2 Mini-Project | Phase 4
"""

import os


class TransactionLogger:
    """
    Context manager to safely open and write to a transaction log file.
    Using this class guarantees that the log file is closed properly
    even if an exception occurs during execution.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None

    def __enter__(self):
        """
        Open the file in append mode.
        If the directory doesn't exist, create it.
        """
        # Ensure directory exists just in case
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        self.file = open(self.file_path, "a", encoding="utf-8")
        return self
        
    def log(self, message: str):
        """Write a string to the open log file with a newline."""
        if self.file and not self.file.closed:
            self.file.write(f"{message}\n")
            
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the file is safely closed when leaving the 'with' block.
        Exceptions will continue to propagate (returns False implicitly).
        """
        if self.file:
            self.file.close()
