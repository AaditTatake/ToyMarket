import pandas as pd


def build_propositions(
    df: pd.DataFrame,
    rsi_low: float = 30.0,
    rsi_high: float = 70.0,
) -> pd.DataFrame:
    """
    Build the six propositional variables:
    P, M, V, R, O, D
    """
    out = df.copy()

    out["P"] = out["Close"] > out["SMA_long"]
    out["M"] = out["SMA_short"] > out["SMA_long"]
    out["V"] = out["Volume"] > out["VolAvg"]
    out["R"] = out["RSI"] < rsi_low
    out["O"] = out["RSI"] > rsi_high
    out["D"] = out["MACD"] > out["MACD_signal"]

    return out


def clean_indicator_warmup(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows where long-window indicators are not ready yet.
    """
    needed = ["SMA_short", "SMA_long", "VolAvg", "RSI", "MACD", "MACD_signal"]
    return df.dropna(subset=needed).copy()
