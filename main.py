import urllib.request, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

QC = "https://kustom.radio-canada.ca/coronavirus/canada_quebec"

last_days = 28

with urllib.request.urlopen(QC) as response:
    data = json.load(response)[0]['History']
    df = pd.json_normalize(data)

    # hospital = int(json.load(response)[0]['Hospitalizations'])
    # icu = int(json.load(response)[0]['IntensiveCare'])

    # Cast types
    df['Date'] = pd.to_datetime(df['Date'])
    numeric_cols = ['Confirmed', 'Deaths', 'Recovered']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # MA calculations make more sense with "today" at the end
    df = df[::-1]
    df.set_index('Date')

    df['Active'] = df.Confirmed - df.Recovered - df.Deaths
    df['Change'] = np.round(df['Active'].diff(), decimals=0)

    df = df.sort_values(by=['Date'], ignore_index=True)

    # Last N days
    df = df.tail(last_days)

    print(df)

    fig = plt.figure(figsize = (25,8))
    p = plt.plot(df['Active'], label="Active")
    # plt.plot(df['Recovered'], label="Recovered")
    plt.plot(df['Change'], label="Change")
    plt.xlabel("Elapsed Days (last %s)" % last_days)
    plt.ylabel("Cases")
    plt.grid(True)

    for i, row in df.iterrows():
        plt.annotate(str(row['Active']), (i, row['Active']))
        plt.annotate(str(row['Change']), (i, row['Change']))

    plt.legend()
    plt.show()
