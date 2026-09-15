"""
test_transaction_logger.py

Unit tests for the TransactionLogger context manager.
DataGrokr PLP Week 2 Mini-Project | Phase 4
"""

import os
import unittest
import tempfile
from src.services.transaction_logger import TransactionLogger


class TestTransactionLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file path
        self.temp_file = os.path.join(tempfile.gettempdir(), "test_tx_log.txt")
        # Ensure it doesn't exist before test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def tearDown(self):
        # Clean up temporary test file
        if os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except Exception:
                pass

    def test_logger_writes_successfully(self):
        """Test the context manager successfully opens and writes to file."""
        with TransactionLogger(self.temp_file) as logger:
            logger.log("Test log entry 1")
            
        self.assertTrue(os.path.exists(self.temp_file))
        with open(self.temp_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), "Test log entry 1")

    def test_logger_closes_on_normal_exit(self):
        """File is closed automatically after leaving the 'with' block."""
        with TransactionLogger(self.temp_file) as logger:
            pass
        self.assertTrue(logger.file.closed)

    def test_logger_closes_on_exception(self):
        """File is closed automatically even when an exception occurs inside the block."""
        logger_ref = None
        try:
            with TransactionLogger(self.temp_file) as logger:
                logger_ref = logger
                raise ValueError("Simulated error")
        except ValueError:
            pass
            
        self.assertIsNotNone(logger_ref)
        self.assertTrue(logger_ref.file.closed)
        
    def test_exception_propagates_out_of_context(self):
        """Exception is NOT suppressed by the context manager (__exit__ returns False)."""
        with self.assertRaises(ValueError) as ctx:
            with TransactionLogger(self.temp_file) as logger:
                raise ValueError("This should bubble out")
                
        self.assertEqual(str(ctx.exception), "This should bubble out")


if __name__ == "__main__":
    unittest.main()
