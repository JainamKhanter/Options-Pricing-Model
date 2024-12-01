#monte carlo simulation:

import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')


def monte_carlo_simulation(start_price, n, mean_return, volatility):
    daily_returns = np.random.normal(mean_return / n, abs(volatility) / np.sqrt(n), n) + 1
    price_series = [start_price]
    for i in range(1, n):
        price_series.append(price_series[i-1] * daily_returns[i-1])
    return price_series

df = pd.read_csv("BSE.csv")
company_index = dict(zip(df.iloc[:,2], df.iloc[:,0]))

def plot_graph(data):
    global company_index
    company_name = data['company']
    company_code = company_index.get(company_name)  # Get the company code from the CSV
    if not company_code:
        print("Company code not found for", company_name)
        return False

    url = f'https://api.upstox.com/v2/historical-candle/{company_code}/day/2024-11-17/2024-04-20'
    response = requests.get(url)
    if response.status_code == 200:
        print("Data received successfully")
    else:
        print("Error")
        return False

    resp = response.json()
    closing = np.array([candle[4] for candle in resp['data']['candles']])
    start_price = closing[0]
    daily_returns = np.diff(closing) / closing[:-1]
    volatility = np.std(daily_returns)
    mean_return = np.mean(daily_returns)
    n = int(data['daysUntilExpiration'])

    # Generate volatility for each day from a normal distribution
    volatility = np.random.normal(abs(volatility), volatility, n)

    # Simulate stock prices
    for _ in range(10):
        simulated_prices = monte_carlo_simulation(start_price, n, mean_return, volatility)
        plt.plot(simulated_prices)

    # Plot the simulated stock prices
    plt.title('Monte Carlo Simulation for Stock Prices')
    plt.xlabel('Days')
    plt.ylabel('Stock Price')
    plt.grid(True)
    plt.savefig(f'static/plot_{0}.png')
    plt.show()
    plt.clf()
    #num+=1
    return True

# data = {
#     'company': 'AARTIIND',
#     'daysUntilExpiration' : 100
# }
# plot_graph(data)