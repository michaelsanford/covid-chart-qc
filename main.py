import urllib.request, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

QC = "https://kustom.radio-canada.ca/coronavirus/canada_quebec"
MONTEREGIE = "https://kustom.radio-canada.ca/coronavirus/canada_quebec_monteregie"

last_days = 42
nth_label = 1

with urllib.request.urlopen(QC) as response:
    data = json.load(response)[0]['History']
    df = pd.json_normalize(data)

    # Cast types
    df['Date'] = pd.to_datetime(df['Date'])
    numeric_cols = ['C', 'D', 'H', 'I', 'R', 'T']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # MA calculations make more sense with "today" at the end
    df = df[::-1]
    df.set_index('Date')

    df['Active'] = df.C - df.R - df.D
    df['Change'] = np.round(df['Active'].diff(), decimals=0)

    df = df.sort_values(by=['Date'], ignore_index=True)

    df['MA'] = df['Active'].rolling(window=7).mean()

    # Last N days
    df = df.tail(last_days)

    print(df)

    fig = plt.figure(figsize = (18,8))
    # p = plt.plot(df['Active'], label="Active")
    # plt.plot(df['R'], label="R")
    plt.plot(df['Change'], label="Change")
    plt.plot(df['H'], label="Hospitalizations")
    plt.plot(df['MA'], label="7 MA")
    plt.xlabel("Elapsed Days (last %s)" % last_days)
    plt.ylabel("Cases")
    plt.grid(True)

    for i, row in df.iterrows():
        if i % nth_label == 0:
            # plt.annotate(str(row['Active']), (i, row['Active']))
            plt.annotate(str(row['Active']), (i, row['MA']))
            plt.annotate(str(row['Change']), (i, row['Change']))

    plt.legend()
    plt.show()
