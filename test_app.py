import unittest
import json
from app3 import app,parse_input, calculate_d1_d2, calculate_option_metrics
from app2 import app 
from colorama import Fore, init

# Initialize colorama for colored outputs
init(autoreset=True)

class TestOptionPricing(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    ### Tests for parse_input ###
    def test_parse_input_success(self):
        """Test parse_input with valid data"""
        data = {
            "underlyingPrice": 100,
            "strikePrice": 100,
            "daysUntilExpiration": 30,
            "interestRate": 5,
            "dividendYield": 2,
            "volatility": 20
        }
        S, K, T, r, q, sigma = parse_input(data)
        self.assertEqual((S, K, T, r, q, sigma), (100, 100, 30 / 365.0, 0.05, 0.02, 0.2))
        print(Fore.GREEN + "parse_input Test 1: Success.")

    def test_parse_input_boundary(self):
        """Test parse_input with minimal inputs"""
        data = {
            "underlyingPrice": 0.01,
            "strikePrice": 100,
            "daysUntilExpiration": 1,
            "interestRate": 0.01,
            "dividendYield": 0.01,
            "volatility": 1
        }
        S, K, T, r, q, sigma = parse_input(data)
        self.assertGreater(S, 0)
        self.assertGreater(T, 0)
        self.assertGreater(sigma, 0)
        print(Fore.GREEN + "parse_input Test 2: Success.")

    def test_parse_input_invalid(self):
        """Test parse_input with missing fields"""
        data = {
            "underlyingPrice": 100,
            "strikePrice": 100,
        }
        with self.assertRaises(KeyError):
            parse_input(data)
        print(Fore.GREEN + "parse_input Test 3: Success (handled missing fields).")

    ### Tests for calculate_d1_d2 ###
    def test_calculate_d1_d2_success(self):
        """Test calculate_d1_d2 with valid inputs"""
        S, K, T, r, q, sigma = 100, 100, 0.0822, 0.05, 0.02, 0.2
        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        self.assertAlmostEqual(d1, 0.145, places=3)
        self.assertAlmostEqual(d2, 0.092, places=3)
        print(Fore.GREEN + "calculate_d1_d2 Test 1: Success.")

    def test_calculate_d1_d2_boundary(self):
        """Test calculate_d1_d2 with near-zero volatility"""
        S, K, T, r, q, sigma = 100, 100, 0.0822, 0.05, 0.02, 0.001
        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        self.assertAlmostEqual(d1, float('inf'), places=1)
        self.assertAlmostEqual(d2, float('inf'), places=1)
        print(Fore.GREEN + "calculate_d1_d2 Test 2: Success.")

    def test_calculate_d1_d2_invalid(self):
        """Test calculate_d1_d2 with invalid input (negative volatility)"""
        with self.assertRaises(ValueError):
            calculate_d1_d2(100, 100, 0.0822, 0.05, 0.02, -0.2)
        print(Fore.GREEN + "calculate_d1_d2 Test 3: Success (handled invalid input).")

    ### Tests for calculate_option_metrics ###
    def test_calculate_option_metrics_success(self):
        """Test calculate_option_metrics with valid inputs"""
        S, K, T, r, q, sigma = 100, 100, 0.0822, 0.05, 0.02, 0.2
        d1, d2 = 0.145, 0.092
        metrics = calculate_option_metrics(S, K, T, r, q, sigma, d1, d2)
        self.assertIn("call", metrics)
        self.assertIn("put", metrics)
        self.assertGreater(metrics["call"], 0)
        print(Fore.GREEN + "calculate_option_metrics Test 1: Success.")

    def test_calculate_option_metrics_boundary(self):
        """Test calculate_option_metrics with near-zero time to expiration"""
        S, K, T, r, q, sigma = 100, 100, 0.0001, 0.05, 0.02, 0.2
        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        metrics = calculate_option_metrics(S, K, T, r, q, sigma, d1, d2)
        self.assertAlmostEqual(metrics["call"], max(S - K, 0), places=2)
        print(Fore.GREEN + "calculate_option_metrics Test 2: Success.")

    def test_calculate_option_metrics_invalid(self):
        """Test calculate_option_metrics with invalid d1 and d2"""
        S, K, T, r, q, sigma = 100, 100, 0.0822, 0.05, 0.02, 0.2
        d1, d2 = float('inf'), float('inf')
        with self.assertRaises(ValueError):
            calculate_option_metrics(S, K, T, r, q, sigma, d1, d2)
        print(Fore.GREEN + "calculate_option_metrics Test 3: Success (handled invalid input).")

if __name__ == '__main__':
    print(Fore.GREEN + "Running Tests...")
    unittest.main(verbosity=2)
