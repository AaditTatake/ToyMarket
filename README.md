# A Propositional Logic Analysis of Rule-Based Trading Signals

This repository contains the code and supporting material for my final project in **MA 385 (Mathematical Logic)**. The project studies how **propositional logic** can be used to model, analyze, and compare simple rule-based trading systems.

The central idea is to encode common technical-analysis conditions as Boolean propositions and use them to construct two signal systems:

- a **naive** rule-based system
- a **refined** rule-based system designed to reduce contradictory outputs

This project is **not** intended to predict market performance or function as a realistic trading strategy. Its purpose is to study how logical structure affects the behavior of a simplified decision system inspired by trading.

---

## Project Overview

The model uses six propositional variables:

- **P**: closing price is above the 20-day simple moving average
- **M**: 5-day simple moving average is above the 20-day simple moving average
- **V**: trading volume is above its 20-day average
- **R**: RSI is below 30
- **O**: RSI is above 70
- **D**: MACD line is above the signal line

These variables are used to encode three common ideas from technical analysis:

- **trend**
- **momentum**
- **confirmation**

The repository also includes a **market simulator** that generates synthetic price and volume data under different market regimes, computes the relevant indicators, converts them into propositional variables, and evaluates both logical systems.

---

## Research Goal

The main question of the project is:

> **Can propositional logic be used to formalize, analyze, and improve a simple rule-based trading decision system?**

More specifically, the project investigates:

- whether the naive system is logically coherent
- whether it can produce conflicting outputs
- whether a refined version behaves more consistently
- how both systems behave under simulated market conditions

---

## Trading Systems

### Naive System

The initial trading rules are:

$$
B_0 = (P \land M \land D)\lor(R \land V)
$$

$$
S_0 = (\neg P \land \neg M \land \neg D)\lor(O \land V)
$$

$$
H_0 = \neg B_0 \land \neg S_0
$$

where:

- $B_0$ = buy
- $S_0$ = sell
- $H_0$ = hold

### Refined System

The refined system adds simple guardrails to reduce contradictory outcomes:

$$
B_1 = \big((P \land M \land D)\lor(R \land V)\big)\land \neg O
$$

$$
S_1 = \big((\neg P \land \neg M \land \neg D)\lor(O \land V)\big)\land \neg R
$$

$$
H_1 = \neg B_1 \land \neg S_1
$$

---

## Simulator Overview

The simulator generates synthetic market data rather than using live or historical prices. This allows the logical systems to be tested in a controlled environment.

At a high level, the simulator will:

1. generate synthetic **price** and **volume** data
2. compute technical indicators from that data
3. convert indicator values into Boolean propositions
4. evaluate the naive and refined systems
5. compare their outputs

The simulator is intended to support multiple market regimes, such as:

- **bullish**
- **bearish**
- **sideways**
- **high-volatility**

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
