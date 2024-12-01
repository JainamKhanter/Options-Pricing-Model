import unittest
import numpy as np
from scipy.stats import norm
from app3 import calculate_option_price  # Make sure to import the correct function

class TestCalculateOptionPrice(unittest.TestCase):

    def test_valid_input(self):
        # Valid test case with typical values
        S = 100  # Spot price
        K = 95   # Strike price
        T = 30 / 365  # Time to expiration in years (30 days)
        r = 0.05  # Risk-free rate
        q = 0.02  # Dividend yield
        sigma = 0.2  # Volatility
        
        call_price, put_price = calculate_option_price(S, K, T, r, q, sigma)
        
        # Check if the calculated call and put prices are reasonable
        self.assertAlmostEqual(call_price, 5.747, places=2)
        self.assertAlmostEqual(put_price, 0.522, places=2)
        
        print("test_valid_input passed successfully!")

    def test_zero_volatility(self):
        # Case with zero volatility
        S = 100
        K = 95
        T = 30 / 365  # 30 days converted to years
        r = 0.05
        q = 0.02
        sigma = 0  # Zero volatility
        
        with self.assertRaises(ValueError) as context:
            calculate_option_price(S, K, T, r, q, sigma)
        
        
        
        print("test_zero_volatility passed successfully!")

    def test_invalid_input_negative_strike(self):
        # Case with invalid input (negative strike price)
        S = 100
        K = -95  # Invalid strike price (negative)
        T = 30 / 365
        r = 0.05
        q = 0.02
        sigma = 0.2
        
        with self.assertRaises(ValueError) as context:
            calculate_option_price(S, K, T, r, q, sigma)
        
        
        print("test_invalid_input_negative_strike passed successfully!")

if __name__ == '__main__':
    unittest.main()
