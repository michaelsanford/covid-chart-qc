# COVID 19 Charting for Québec

Pandas experiment to chart some COVID data.

## Quickstart

```powershell
pip install -r requirements.txt
py main.py
```

## What is this?

A silly late-night experiment with Pandas to make my own charts.

Probably don't use it for anything serious.

# `History` Data Structure

```json
"History": [
    {
        "Date": "2020-10-15",
        "C": "89963",
        "D": "6005",
        "H": "493",
        "I": "83",
        "P": "0",
        "R": "75467",
        "T": "2713686"
    }
]
```

| Key | Type | Represents |
|-|-|-|
|`C`| `Number` | Confirmed Cases (Total) |
|`D`| `Number` | Deaths (Total) |
|`H`| `Number` | Hospitalizations (Total, including ICU) |
|`I`| `Number` | ICU Admissions (Total) |
|`P`| `Float`  | _(Unknown)_ |
|`R`| `Number` | Recoveries (Total) |
|`T`| `Number` | Tests Conducted (Total, delayed 48h) |
