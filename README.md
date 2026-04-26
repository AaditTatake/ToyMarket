# A Propositional Logic Analysis of Rule-Based Trading Signals

This repository contains the code and supporting material for a project in **MA 385 (Mathematical Logic)** exploring how **propositional logic** can be used to model and analyze a simple rule-based trading system.

The central idea is to represent common technical-analysis conditions as Boolean propositions and then use those propositions to construct and compare two trading systems:

- a **naive** rule-based system
- a **refined** rule-based system designed to reduce contradictory outputs

The project is **not** intended to predict market performance or serve as a realistic trading strategy. Instead, it studies how logical structure affects the behavior of a simple decision system inspired by trading.

---

## Project Overview

This project models trading decisions using six propositional variables:

- **P**: closing price is above the 20-day SMA  
- **M**: 5-day SMA is above the 20-day SMA  
- **V**: trading volume is above its 20-day average  
- **R**: RSI is below 30  
- **O**: RSI is above 70  
- **D**: MACD line is above the signal line  

These variables are used to encode ideas from technical analysis such as:

- **trend**
- **momentum**
- **volume confirmation**
- **mean reversion**

The repository also includes a **market simulator** that generates synthetic price and volume data under different market regimes, computes technical indicators from that data, converts them into propositional variables, and evaluates the naive and refined trading systems.

---

## Research Goal

The main question of the project is:

> **Can propositional logic be used to formalize, analyze, and improve a simple rule-based trading decision system?**

More specifically, the project studies:

- whether the naive system is logically coherent
- whether it can produce conflicting outputs
- whether a refined version behaves more consistently
- how both systems behave under simulated market conditions

---

## Trading Systems

### Naive System

The initial trading rules are:

\[
B_0 = (P \land M \land D)\lor(R \land V)
\]

\[
S_0 = (\neg P \land \neg M \land \neg D)\lor(O \land V)
\]

\[
H_0 = \neg B_0 \land \neg S_0
\]

where:

- \(B_0\) = buy
- \(S_0\) = sell
- \(H_0\) = hold

### Refined System

The refined system adds simple guardrails to reduce contradiction:

\[
B_1 = \big((P \land M \land D)\lor(R \land V)\big)\land \neg O
\]

\[
S_1 = \big((\neg P \land \neg M \land \neg D)\lor(O \land V)\big)\land \neg R
\]

\[
H_1 = \neg B_1 \land \neg S_1
\]

---

## Repository Goals

This repository is intended to support the following tasks:

- simulate synthetic market data
- compute technical indicators from that data
- map indicator values to propositional variables
- evaluate naive and refined trading systems
- compare the outputs of the two systems
- study logical behavior such as satisfiability and contradiction

---

## Planned Features

- [ ] price and volume simulator
- [ ] bullish / bearish / sideways market regimes
- [ ] SMA, RSI, and MACD computation
- [ ] propositional-variable construction
- [ ] naive-system evaluation
- [ ] refined-system evaluation
- [ ] summary statistics for buy / sell / hold / conflict counts
- [ ] plots of simulated price and signal behavior

---

## Proposed Repository Structure

```text
.
├── README.md
├── src/
│   ├── simulator.py
│   ├── indicators.py
│   ├── propositions.py
│   ├── logic_models.py
│   └── main.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── outputs/
│   ├── figures/
│   └── tables/
└── paper/
    └── final_report.tex
