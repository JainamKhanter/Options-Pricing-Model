from flask import Flask, render_template,request, jsonify
import numpy as np
from scipy.stats import norm
import traceback
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.parse
import numpy as np
import pandas as pd
import requests
from monte import plot_graph

num = 0

# from flask_wtf.csrf import generate_csrf
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

# app.config['SECRET_KEY'] = 'jainam'
# csrf = CSRFProtect(app)

@app.route('/')
def index():
    
    return render_template('topsj.html')

@app.route('/initdb')
def init_db():
    create_tables()
    return 'Database initialized'

@app.route('/Optionsinfo')
def info():
    return render_template('/Optionsinfo.html')

@app.route('/blackscholes')
def info12():
    return render_template('/blackscholes.html')

@app.route('/about')
def info123():
    return render_template('/aboutus.html')

@app.route("/monte_carlo", methods=['POST'])
def plot_monte_graph():
    
    data = request.get_json()
    status = plot_graph(data)
    plot_filename = f"/static/plot_0.png"
    
    return jsonify({"status":status, "plot_filename":plot_filename})


# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/login', methods=['GET'])
# def login():
#     # csrf_token = generate_csrf()
#     return render_template('login.html', csrf_token=csrf_token)

@app.route('/index')
def rel():
    return render_template('index.html')

@app.route('/index2')
def rel1():
    return render_template('index2.html')

@app.route('/monte')
def mon():
    return render_template('montecarlo.html')


@app.route('/calculate', methods=['POST'])
def calculate_option_price():
    try:
        data = request.get_json()
        
        # S = float(data['underlyingPrice'])
        company_name = data['company']
        K = float(data['strikePrice'])
        T = float(data['daysUntilExpiration']) / 365.0
        r = float(data['interestRate']) / 100.0
        q = float(data['dividendYield']) / 100.0 
        # sigma = float(data['volatility']) / 100.0
        df = pd.read_csv('BSE.csv')
        company_index = dict(zip(df.iloc[:, 2], df.iloc[:, 0]))
        # print(company_index['AARTIIND'])

        api_key = '70c3e98c-b4cf-43dd-8985-8f1fb7bedb8c'
        api_secret = 'namont60ag'
        redir_url = urllib.parse.quote('http://127.0.0.1:5000', safe="")

        rurl = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={api_key}&redirect_uri={redir_url}'
        #print(rurl)
        code = 'YJ_FnT'


        auth_url = 'https://api.upstox.com/v2/login/authorization/token'
        # print("hi")
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'code': f'{code}',
            'client_id': f'{api_key}',
            'client_secret': f'{api_secret}',
            'redirect_uri': 'http://127.0.0.1:5000',
            'grant_type': 'authorization_code',
        }
        # print("hi")
        
        # response = requests.post(auth_url, headers=headers, data=data)
       
        # print("hi")
        # print(response.status_code)
        # print(response.json())
        # company_name = 'AARTIIND'
        # print(c)
       
        url1 = f'https://api.upstox.com/v2/historical-candle/{company_index[company_name]}/day/2024-11-17/2024-02-19'
        # url1 = f'https://api.upstox.com/v2/historical-candle/NSE_EQ%7CINE848E01016/day/2024-04-26/2024-02-19'
        headers = {
            'Accept': 'application/json'
        }
        
        response = requests.get(url1, headers=headers)
        print("hi")
        # Check the response status
        # if response.status_code == 200:
        #     # Do something with the response data (e.g., print it)
        #     #print(response.json())
        #     print()
            
        # else:
            # Print an error message if the request was not successful
            # print(f"Error: {response.status_code} - {response.text}")
        resp = response.json()
        high = np.array([candle[2] for candle in resp['data']['candles']])
        lows = np.array([candle[3] for candle in resp['data']['candles']])
        open = np.array([candle[1] for candle in resp['data']['candles']])
        close = np.array([candle[4] for candle in resp['data']['candles']])
        S = close[0]
        print(S)   
        log_returns = np.diff(np.log(close))

        
        sigma = 100*np.std(log_returns)
        print(sigma)
        

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
            gamma=gamma, vega=vega,
            uprice=S
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
    
@app.route('/calculate1', methods=['POST'])
def calculate_option_price1():
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
      return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            return render_template('index.html', username=username)
        else:
            return render_template('login.html', error='Invalid username or password')
    
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
