import unittest
from app3 import calculate_d1_d2  # Ensure this imports the correct function

class TestCalculateD1D2(unittest.TestCase):

    def test_valid_input(self):
        # Valid test case with typical values
        S = 100
        K = 95
        T = 30 / 365  # 30 days converted to years
        r = 0.05
        q = 0.02
        sigma = 0.2
        
        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        
        # Check if the values are approximately correct to 3 decimal places
        self.assertAlmostEqual(d1, 0.966, places=3)
        self.assertAlmostEqual(d2, 0.9089, places=3)
        print("test_valid_input passed successfully!")

    def test_zero_volatility(self):
        # Case with zero volatility
        S = 100
        K = 95
        T = 30 / 365
        r = 0.05
        q = 0.02
        sigma = 0
        
        
        
        # Check if both d1 and d2 are 'inf' when volatility is zero
        
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        
        print("test_zero_volatility passed successfully!")

    def test_invalid_input(self):
        # Case with invalid spot price (negative)
        S = -100  # Invalid spot price
        K = 95
        T = 30 / 365
        r = 0.05
        q = 0.02
        sigma = 0.2
        
        
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        print("test_invalid_input passed successfully!")

    def test_zero_time(self):
        # Case where time to expiration is zero
        S = 100
        K = 95
        T = 0  # Zero time to expiration
        r = 0.05
        q = 0.02
        sigma = 0.2
        
        
        
        
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        print("test_zero_time passed successfully!")

    def test_invalid_sigma(self):
        # Case with invalid volatility (negative)
        S = 100
        K = 95
        T = 30 / 365
        r = 0.05
        q = 0.02
        sigma = -0.2  # Invalid negative volatility
        
        # Test for ValueError to be raised
        with self.assertRaises(ValueError):
            calculate_d1_d2(S, K, T, r, q, sigma)
        print("test_invalid_sigma passed successfully!")

if __name__ == '__main__':
    unittest.main()
