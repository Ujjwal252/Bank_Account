"""
test_decorators.py

Unit tests for the custom decorators.
DataGrokr PLP Week 2 Mini-Project | Phase 4
"""

import unittest
from src.services.decorators import log_transaction

class TestDecorators(unittest.TestCase):
    
    def test_decorator_preserves_metadata(self):
        """functools.wraps preserves function name and docstring."""
        @log_transaction
        def sample_func():
            """Sample docstring."""
            pass
            
        self.assertEqual(sample_func.__name__, "sample_func")
        self.assertEqual(sample_func.__doc__, "Sample docstring.")

    def test_decorator_executes_and_returns(self):
        """Decorator successfully runs function and returns its result."""
        @log_transaction
        def add(a, b):
            return a + b
            
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, b=5), 15)

    def test_decorator_propagates_exceptions(self):
        """Exceptions are not swallowed by the decorator."""
        @log_transaction
        def failing_func():
            raise ValueError("Something went wrong")
            
        with self.assertRaises(ValueError) as ctx:
            failing_func()
        self.assertEqual(str(ctx.exception), "Something went wrong")

if __name__ == "__main__":
    unittest.main()
