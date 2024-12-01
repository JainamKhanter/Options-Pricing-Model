import unittest
from app3 import calculate_greeks, calculate_d1_d2  # Ensure this imports the correct functions

class TestCalculateGreeks(unittest.TestCase):

    def test_valid_input(self):
       
        S = 100  # Spot price
        K = 95   # Strike price
        T = 30 / 365  # Time to expiration in years (30 days)
        r = 0.05  # Risk-free rate
        q = 0.02  # Dividend yield
        sigma = 0.2  # Volatility
        
        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)  
        greeks = calculate_greeks(S, K, T, r, q, sigma, d1, d2)
        
        # Check if the Greeks values are approximately correct
        self.assertAlmostEqual(greeks["call_delta"], 0.8316, places=3)
        self.assertAlmostEqual(greeks["put_delta"], -0.1666, places=3)
        self.assertAlmostEqual(greeks["call_theta"], -0.0299, places=3)
        self.assertAlmostEqual(greeks["put_theta"], -0.0224, places=3)
        self.assertAlmostEqual(greeks["call_rho"], 0.0636, places=3)
        self.assertAlmostEqual(greeks["put_rho"], -0.0141, places=3)
        self.assertAlmostEqual(greeks["gamma"], 0.0435, places=3)
        self.assertAlmostEqual(greeks["vega"], 0.0715, places=3)
        
        print("test_valid_input passed successfully!")

    def test_zero_volatility(self):
        # Case with zero volatility
        S = 100
        K = 95
        T = 30 / 365  # 30 days converted to years
        r = 0.05
        q = 0.02
        sigma = 0  # Zero volatility
        
        
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        
            
        
        # Check if all Greeks are 'inf' when volatility is zero
        
        
        print("test_zero_volatility passed successfully!")

    def test_invalid_input(self):
        # Case with invalid input (negative strike price)
        S = 100
        K = -95  # Invalid strike price (negative)
        T = 30 / 365
        r = 0.05
        q = 0.02
        sigma = 0.2
        
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        
        print("test_invalid_input passed successfully!")

if __name__ == '__main__':
    unittest.main()
