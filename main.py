import urllib.request, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

QC = "https://kustom.radio-canada.ca/coronavirus/canada_quebec"

with urllib.request.urlopen(QC) as response:
    data = json.load(response)[0]['History']
    df = pd.json_normalize(data)

    # Cast types
    df['Date'] = pd.to_datetime(df['Date'])
    numeric_cols = ['Confirmed', 'Deaths', 'Recovered']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # MA calculations make more sense with "today" at the end
    df = df[::-1]
    df.set_index('Date')
    # df.reindex()

    df['Active'] = df.Confirmed - df.Recovered - df.Deaths

    weights = np.arange(1,6)
    wma10 = df.Active.rolling(5).apply(lambda act: np.dot(act, weights)/weights.sum(), raw=True)
    df['5_WMA'] = np.round(wma10, decimals=1)

    # df['5_SMA'] = df.Active.rolling(5).mean()

    df['New'] = np.round(df['Active'] - df['Active'].shift(), decimals=0)

    df['EMA_New'] = df.iloc[:,-1].ewm(span=7, adjust=True).mean()

    df['RoC'] = df['Active'].diff()

    df = df.sort_values(by=['Date'], ignore_index=True)

    # Last N days
    df = df.tail(45)

    print(df)

    plt.figure(figsize = (12,6))
    # plt.plot(df['Active'], label="Active")
    # plt.plot(df['Recovered'], label="Recovered")
    # plt.plot(df['RoC'], label="Rate of Change")
    plt.plot(df['5_WMA'], label="5-Day WMA")
    plt.plot(df['New'], label="New Cases")
    plt.plot(df['EMA_New'], label="3 EMA (New Cases)")
    plt.xlabel("Elapsed Days")
    plt.ylabel("Cases")
    plt.grid(True)
    plt.legend()
    plt.show()
