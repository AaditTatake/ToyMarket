import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from simulator import simulate_market
from indicators import add_indicators
from propositions import build_propositions, clean_indicator_warmup
from logic_models import evaluate_naive, evaluate_refined, summarize_outputs


def get_user_inputs() -> dict:
    print("=== Rule-Based Trading Signal Simulator ===")
    regime = input("Choose regime [bull / bear / sideways / volatile] (default: sideways): ").strip() or "sideways"

    n_days_str = input("Number of days (default: 250): ").strip()
    n_days = int(n_days_str) if n_days_str else 250

    start_price_str = input("Starting price (default: 100): ").strip()
    start_price = float(start_price_str) if start_price_str else 100.0

    base_volume_str = input("Base volume (default: 1000000): ").strip()
    base_volume = float(base_volume_str) if base_volume_str else 1_000_000.0

    short_sma_str = input("Short SMA window (default: 5): ").strip()
    short_sma = int(short_sma_str) if short_sma_str else 5

    long_sma_str = input("Long SMA window (default: 20): ").strip()
    long_sma = int(long_sma_str) if long_sma_str else 20

    rsi_low_str = input("RSI lower threshold (default: 30): ").strip()
    rsi_low = float(rsi_low_str) if rsi_low_str else 30.0

    rsi_high_str = input("RSI upper threshold (default: 70): ").strip()
    rsi_high = float(rsi_high_str) if rsi_high_str else 70.0

    seed_str = input("Random seed (default: 42): ").strip()
    seed = int(seed_str) if seed_str else 42

    return {
        "regime": regime,
        "n_days": n_days,
        "start_price": start_price,
        "base_volume": base_volume,
        "short_sma": short_sma,
        "long_sma": long_sma,
        "rsi_low": rsi_low,
        "rsi_high": rsi_high,
        "seed": seed,
    }


def print_summary(summary: dict[str, int]) -> None:
    print("\n=== Output Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")


def make_sample_table(df: pd.DataFrame, n_rows: int = 12) -> pd.DataFrame:
    cols = [
        "Close", "Volume", "SMA_short", "SMA_long", "RSI", "MACD", "MACD_signal",
        "P", "M", "V", "R", "O", "D",
        "B0", "S0", "H0", "Conflict0",
        "B1", "S1", "H1", "Conflict1",
    ]
    sample = df[cols].tail(n_rows).copy()
    return sample.round(
        {
            "Close": 2,
            "SMA_short": 2,
            "SMA_long": 2,
            "RSI": 2,
            "MACD": 4,
            "MACD_signal": 4,
        }
    )


def plot_results(df: pd.DataFrame, title_suffix: str) -> None:
    x = df.index.to_list()

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

    # Price + SMAs
    axes[0].plot(x, df["Close"].to_numpy(), label="Close")
    axes[0].plot(x, df["SMA_short"].to_numpy(), label="Short SMA")
    axes[0].plot(x, df["SMA_long"].to_numpy(), label="Long SMA")
    axes[0].set_title(f"Simulated Price and SMAs ({title_suffix})")
    axes[0].legend()

    # RSI
    axes[1].plot(x, df["RSI"].to_numpy(), label="RSI")
    axes[1].axhline(30, linestyle="--")
    axes[1].axhline(70, linestyle="--")
    axes[1].set_title("RSI")
    axes[1].legend()

    # MACD
    axes[2].plot(x, df["MACD"].to_numpy(), label="MACD")
    axes[2].plot(x, df["MACD_signal"].to_numpy(), label="Signal")
    axes[2].set_title("MACD")
    axes[2].legend()

    plt.tight_layout()
    plt.show()

def make_output_dir() -> Path:
    out_dir = Path("outputs") / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def save_summary_csv(summary: dict[str, int], out_dir: Path, prefix: str) -> None:
    summary_df = pd.DataFrame(
        {"metric": list(summary.keys()), "value": list(summary.values())}
    )
    summary_df.to_csv(out_dir / f"{prefix}_summary.csv", index=False)


def save_sample_table_csv(sample: pd.DataFrame, out_dir: Path, prefix: str) -> None:
    sample.to_csv(out_dir / f"{prefix}_sample_table.csv")


def save_full_results_csv(df: pd.DataFrame, out_dir: Path, prefix: str) -> None:
    df.to_csv(out_dir / f"{prefix}_full_results.csv")

def main() -> None:
    params = get_user_inputs()

    df = simulate_market(
        n_days=params["n_days"],
        regime=params["regime"],
        start_price=params["start_price"],
        base_volume=params["base_volume"],
        seed=params["seed"],
    )

    df = add_indicators(
        df,
        short_sma=params["short_sma"],
        long_sma=params["long_sma"],
        volume_window=params["long_sma"],
        rsi_window=14,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
    )

    df = build_propositions(
        df,
        rsi_low=params["rsi_low"],
        rsi_high=params["rsi_high"],
    )

    df = clean_indicator_warmup(df)
    df = evaluate_naive(df)
    df = evaluate_refined(df)

    summary = summarize_outputs(df)
    print_summary(summary)

    print("\n=== Sample Table (last 12 rows) ===")
    sample = make_sample_table(df, n_rows=12)
    pd.set_option("display.max_columns", None)
    print(sample)

    # Save outputs
    out_dir = make_output_dir()
    prefix = f"{params['regime']}_{params['n_days']}d_seed{params['seed']}"

    save_summary_csv(summary, out_dir, prefix)
    save_sample_table_csv(sample, out_dir, prefix)
    save_full_results_csv(df, out_dir, prefix)

    print(f"\nSaved CSV files to: {out_dir.resolve()}")
    print(f"- {prefix}_summary.csv")
    print(f"- {prefix}_sample_table.csv")
    print(f"- {prefix}_full_results.csv")

    plot_results(df, title_suffix=params["regime"])


if __name__ == "__main__":
    main()
