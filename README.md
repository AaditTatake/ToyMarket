# A Propositional Logic Analysis of Rule-Based Trading Signals

This repository contains the Python program used for my MA 385 final project, **A Propositional Logic Analysis of Rule-Based Trading Signals**.

The program uses a simplified trading-signal model as an example of a rule-based decision system. It generates simulated market data, computes technical indicators, converts those indicators into propositional variables, and then compares two logical trading systems:

1. a **naive system**, which can sometimes produce contradictory outputs, and  
2. a **refined system**, which adds logical restrictions to remove those contradictions.

This project is **not financial advice** and is not intended to predict real market behavior. The purpose is to study how propositional logic can be used to model, analyze, and improve a structured decision system.

---

## How to Run the Program

First, install the required packages:

```bash
pip install -r requirements.txt
```

Then run the program from the project folder:

```bash
python main.py
```

The program is interactive. It will ask you to enter several parameters for the simulation. If you want to use the default value for a parameter, just press **Enter**.

Example:

```text
=== Rule-Based Trading Signal Simulator ===
Choose regime [bull / bear / sideways / volatile] (default: sideways):
Number of days (default: 250):
Starting price (default: 100):
Base volume (default: 1000000):
Short SMA window (default: 5):
Long SMA window (default: 20):
RSI lower threshold (default: 30):
RSI upper threshold (default: 70):
Random seed (default: 42):
```

If you press **Enter** for every prompt, the program will run the default simulation.

---

## What Each Parameter Means

### `regime`

This controls the type of synthetic market being simulated.

The available choices are:

```text
bull
bear
sideways
volatile
```

Use `bull` to simulate a market with an upward drift.

Use `bear` to simulate a market with a downward drift.

Use `sideways` to simulate a market with no strong upward or downward trend.

Use `volatile` to simulate a market with larger price swings.

The default value is:

```text
sideways
```

---

### `n_days`

This is the number of business days to simulate.

The default value is:

```text
250
```

The simulator requires at least 50 days because the technical indicators need enough data before they become meaningful. For example, a 20-day moving average cannot be computed properly until enough prior prices exist.

---

### `start_price`

This is the starting price of the simulated asset.

The default value is:

```text
100
```

For example, if the starting price is 100, the simulated price series begins at 100 and then evolves according to the chosen market regime.

---

### `base_volume`

This is the typical trading volume around which the program generates simulated volume data.

The default value is:

```text
1000000
```

The simulator does not keep volume perfectly constant. It adds random variation and occasional volume spikes, which allows the model to test whether volume is above or below its moving average.

---

### `short_sma`

This is the window length for the short simple moving average.

The default value is:

```text
5
```

The short SMA is used to represent shorter-term price movement. In this project, it is compared against the long SMA to help determine whether the market has positive trend alignment.

It is used in the proposition:

```text
M = short SMA is above long SMA
```

---

### `long_sma`

This is the window length for the long simple moving average.

The default value is:

```text
20
```

The long SMA is used as the main trend baseline. The program checks whether the current closing price is above this long SMA.

It is used in the propositions:

```text
P = closing price is above long SMA
M = short SMA is above long SMA
```

The program also uses this same window length when computing average volume.

---

### `rsi_low`

This is the lower RSI threshold.

The default value is:

```text
30
```

The RSI, or relative strength index, is a momentum indicator. In this project, a low RSI value represents an oversold condition.

The parameter `rsi_low` is used in the proposition:

```text
R = RSI is below rsi_low
```

With the default value, this means:

```text
R = RSI is below 30
```

---

### `rsi_high`

This is the upper RSI threshold.

The default value is:

```text
70
```

A high RSI value represents an overbought condition.

The parameter `rsi_high` is used in the proposition:

```text
O = RSI is above rsi_high
```

With the default value, this means:

```text
O = RSI is above 70
```

---

### `seed`

This is the random seed used by the simulator.

The default value is:

```text
42
```

The seed controls the random numbers used to generate the simulated market data. If you use the same seed with the same parameters, you should get the same simulated data again. If you change the seed, the program will generate a different simulated market path.

---

## Propositional Variables

After generating the simulated market data and computing the indicators, the program converts each trading day into six propositional variables.

| Variable | Meaning |
|---|---|
| `P` | Closing price is above the long SMA |
| `M` | Short SMA is above the long SMA |
| `V` | Volume is above its moving average |
| `R` | RSI is below the lower threshold |
| `O` | RSI is above the upper threshold |
| `D` | MACD line is above the MACD signal line |

Each variable is either `True` or `False` for each simulated trading day.

---

## Logical Trading Systems

The program compares two systems: a naive system and a refined system.

---

### Naive System

The naive buy rule is:

```text
B0 = (P and M and D) or (R and V)
```

This means the system buys if either:

1. price, moving averages, and MACD all show bullish trend behavior, or  
2. RSI is oversold and volume is elevated.

The naive sell rule is:

```text
S0 = (not P and not M and not D) or (O and V)
```

This means the system sells if either:

1. price, moving averages, and MACD all show bearish behavior, or  
2. RSI is overbought and volume is elevated.

The naive hold rule is:

```text
H0 = not B0 and not S0
```

This means the system holds only when neither the buy rule nor the sell rule is true.

The possible problem with the naive system is that `B0` and `S0` can both be true on the same day. That creates a logical conflict: the model is simultaneously saying to buy and sell.

The program records this with:

```text
Conflict0 = B0 and S0
```

---

### Refined System

The refined system modifies the naive system by adding simple logical guardrails.

The refined buy rule is:

```text
B1 = ((P and M and D) or (R and V)) and not O
```

This means the refined system will not issue a buy signal if the market is also classified as overbought.

The refined sell rule is:

```text
S1 = ((not P and not M and not D) or (O and V)) and not R
```

This means the refined system will not issue a sell signal if the market is also classified as oversold.

The refined hold rule is:

```text
H1 = not B1 and not S1
```

The refined system is designed to remove the most obvious buy/sell contradictions.

The program records refined-system conflicts with:

```text
Conflict1 = B1 and S1
```

Ideally, the refined system should produce zero conflicts.

---

## Program Output

After the simulation runs, the program prints two main things:

1. an output summary, and  
2. a sample table showing the last 12 rows of the simulation.

The output summary reports counts for:

```text
B0_buy_count
S0_sell_count
H0_hold_count
Conflict0_count
B1_buy_count
S1_sell_count
H1_hold_count
Conflict1_count
```

These counts show how many times each system produced buy, sell, hold, or conflict outputs.

---

## Saved CSV Files

The program saves CSV files in:

```text
outputs/tables/
```

For example, if you run a sideways simulation with 250 days and seed 42, the output files will be named:

```text
sideways_250d_seed42_summary.csv
sideways_250d_seed42_sample_table.csv
sideways_250d_seed42_full_results.csv
```

### Summary CSV

The summary CSV contains the total output counts for the naive and refined systems.

### Sample Table CSV

The sample table CSV contains the last 12 rows of the simulation, including prices, indicators, propositions, and logical outputs.

### Full Results CSV

The full results CSV contains every simulated row, including:

- generated market data,
- computed indicators,
- propositional variables,
- naive-system outputs,
- refined-system outputs.

---

## Plot

At the end of the program, a plot window opens with three panels:

1. simulated closing price with short and long SMAs,
2. RSI with threshold lines,
3. MACD and MACD signal line.

This plot helps visualize the simulated data that produced the logical outputs.

If the program seems paused at the end, close the plot window. The program may not fully exit until the plot window is closed.

---

## File Overview

### `main.py`

Runs the full program. It asks for user inputs, calls the simulator, computes indicators, builds propositions, evaluates both logical systems, saves CSV files, and displays the plot.

### `simulator.py`

Generates synthetic OHLCV market data. OHLCV means:

```text
Open, High, Low, Close, Volume
```

The simulated price data is generated using random log returns based on the chosen market regime.

### `indicators.py`

Computes the technical indicators used by the model:

- simple moving averages,
- RSI,
- exponential moving averages,
- MACD,
- MACD signal line,
- MACD histogram.

### `propositions.py`

Converts the indicator values into Boolean propositional variables:

```text
P, M, V, R, O, D
```

It also removes early rows where indicators are not ready yet.

### `logic_models.py`

Evaluates the naive and refined logical trading systems.

It also summarizes the output counts for buy, sell, hold, and conflict conditions.

### `requirements.txt`

Lists the Python packages needed to run the project.

---

## Typical Runs Used for the Project

For the project writeup, the main simulations used:

```text
n_days: 250
start_price: 100
base_volume: 1000000
short_sma: 5
long_sma: 20
rsi_low: 30
rsi_high: 70
seed: 42
```

The regimes compared were:

```text
bull
sideways
volatile
```

To reproduce those results, run the program once for each of those regimes while keeping the other parameters the same.
