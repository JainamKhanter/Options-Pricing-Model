import numpy as np
from scipy.stats import norm
from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_option_price(S, K, T, r, q, sigma):
    try:
        # Check for invalid inputs
        if S <= 0 or K <= 0 or T <= 0 or r < 0 or q < 0 or sigma < 0:
            raise ValueError("Invalid input: All input values must be positive, and volatility must be non-negative.")
        
        # Check if volatility or time to expiration is zero
        if sigma == 0 or T == 0:
            raise ValueError("Invalid input: Volatility and time to expiration must be greater than zero.")

        # Calculate d1 and d2
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Option price calculations
        call = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        put = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        
        # Return the option prices
        return call, put
    except ZeroDivisionError:
        # Handle division by zero gracefully
        raise ValueError("Error in option price calculation: Division by zero encountered.")
    except Exception as e:
        # Catch any other unexpected errors and raise a ValueError with the exception message
        raise ValueError(f"Error in option price calculation: {str(e)}")
    
def calculate_d1_d2(S, K, T, r, q, sigma):
    try:
        # Check for invalid inputs
        if S <= 0 or K <= 0 or T <= 0 or r < 0 or q < 0 or sigma < 0:
            raise ValueError("Invalid input: All input values must be positive, and volatility must be non-negative.")
        
        if sigma == 0 or T == 0:
            raise ValueError("Invalid input: Volatility and time to expiration must be greater than zero.")

        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Check if d1 or d2 is NaN or infinite
        if np.isnan(d1) or np.isnan(d2) or np.isinf(d1) or np.isinf(d2):
            raise ValueError("Error: d1 or d2 calculation resulted in NaN or infinity.")

        return d1, d2
    except ZeroDivisionError:
        raise ValueError("Error in d1 and d2 calculation: Division by zero encountered.")
    except Exception as e:
        raise ValueError(f"Error in d1 and d2 calculation: {str(e)}")

def calculate_greeks(S, K, T, r, q, sigma, d1, d2):
    try:
        # Check for invalid inputs
        if S <= 0 or K <= 0 or T <= 0 or r < 0 or q < 0 or sigma < 0:
            raise ValueError("Invalid input: All input values must be positive, and volatility must be non-negative.")
        
        if sigma == 0 or T == 0:
            raise ValueError("Invalid input: Volatility and time to expiration must be greater than zero.")

        call_delta = np.exp(-q * T) * norm.cdf(d1)
        put_delta = np.exp(-q * T) * (norm.cdf(d1) - 1)

        call_theta = (-(S * sigma * np.exp(-q * T) * norm.pdf(d1) / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2) + q * S * np.exp(-q * T) * norm.cdf(d1)) / 365
        put_theta = (-(S * sigma * np.exp(-q * T) * norm.pdf(d1) / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * norm.cdf(-d2) - q * S * np.exp(-q * T) * norm.cdf(-d1)) / 365

        call_rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        put_rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

        gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) / 100

        # Check if any Greek value is negative, NaN, or infinite
       

        return {
            "call_delta": call_delta,
            "put_delta": put_delta,
            "call_theta": call_theta,
            "put_theta": put_theta,
            "call_rho": call_rho,
            "put_rho": put_rho,
            "gamma": gamma,
            "vega": vega
        }
    except ZeroDivisionError:
        raise ValueError("Error in Greeks calculation: Division by zero encountered.")
    except Exception as e:
        raise ValueError(f"Error in Greeks calculation: {str(e)}")

@app.route('/calculate_d1_d2', methods=['POST'])
def d1_d2():
    try:
        data = request.get_json()
        S = float(data['underlyingPrice'])
        K = float(data['strikePrice'])
        T = float(data['daysUntilExpiration']) / 365.0
        r = float(data['interestRate']) / 100.0
        q = float(data['dividendYield']) / 100.0
        sigma = float(data['volatility']) / 100.0

        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        return jsonify(d1=d1, d2=d2)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/calculate_greeks', methods=['POST'])
def greeks():
    try:
        data = request.get_json()
        S = float(data['underlyingPrice'])
        K = float(data['strikePrice'])
        T = float(data['daysUntilExpiration']) / 365.0
        r = float(data['interestRate']) / 100.0
        q = float(data['dividendYield']) / 100.0
        sigma = float(data['volatility']) / 100.0

        d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
        greek_values = calculate_greeks(S, K, T, r, q, sigma, d1, d2)

        return jsonify(greeks=greek_values)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
