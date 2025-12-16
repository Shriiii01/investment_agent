"""
Unit tests for utility functions.
"""

import unittest
from utils import validate_stock_symbol, format_stock_symbol


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_stock_symbol_valid(self):
        """Test validation of valid stock symbols."""
        self.assertTrue(validate_stock_symbol("AAPL"))
        self.assertTrue(validate_stock_symbol("MSFT"))
        self.assertTrue(validate_stock_symbol("GOOGL"))
        self.assertTrue(validate_stock_symbol("TSLA"))
    
        """Test formatting of stock symbols."""
        self.assertEqual(format_stock_symbol("aapl"), "AAPL")
        self.assertEqual(format_stock_symbol("  msft  "), "MSFT")
        self.assertEqual(format_stock_symbol(""), "")


if __name__ == "__main__":
    unittest.main()

