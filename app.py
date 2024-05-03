from flask import Flask, render_template,request, jsonify
import numpy as np
from scipy.stats import norm
import traceback
# from flask_wtf.csrf import generate_csrf
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# app.config['SECRET_KEY'] = 'jainam'
# csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('topsj.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/login', methods=['GET'])
def login():
    # csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)

@app.route('/index')
def rel():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate_option_price():
    try:
        data = request.get_json()
        S = float(data['underlyingPrice'])
        K = float(data['strikePrice'])
        T = float(data['daysUntilExpiration']) / 365.0
        r = float(data['interestRate']) / 100.0
        q = float(data['dividendYield']) / 100.0 
        sigma = float(data['volatility']) / 100.0

        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        call = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        put = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        call_delta = np.exp(-q * T) * norm.cdf(d1)
        put_delta = np.exp(-q * T) * (norm.cdf(d1) - 1)
        call_theta = (-(S * sigma * np.exp(-q * T)*norm.pdf(d1) / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2) + q*S*np.exp(-q*T)*norm.cdf(d1))/365#change per calender day
        put_theta =  (-(S * sigma * np.exp(-q * T)*norm.pdf(d1) / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * norm.cdf(-d2) -q*S*np.exp(-q*T)*norm.cdf(-d1))/365#change per calender day
        call_rho = K * T * np.exp(-r * T) * norm.cdf(d2)/100
        put_rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)/100
        gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)/100

        return jsonify(
            call=call, put=put,
            call_delta=call_delta, put_delta=put_delta,
            call_theta=call_theta, put_theta=put_theta,
            call_rho=call_rho, put_rho=put_rho,
            gamma=gamma, vega=vega
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
