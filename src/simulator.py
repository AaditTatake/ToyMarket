import numpy as np
import pandas as pd


def get_regime_params(regime: str) -> tuple[float, float]:
    regime = regime.lower().strip()
    if regime == "bull":
        return 0.0010, 0.012
    if regime == "bear":
        return -0.0010, 0.015
    if regime == "sideways":
        return 0.0000, 0.010
    if regime == "volatile":
        return 0.0000, 0.025
    raise ValueError("Regime must be one of: bull, bear, sideways, volatile")


def simulate_market(
    n_days: int = 200,
    regime: str = "sideways",
    start_price: float = 100.0,
    base_volume: float = 1_000_000.0,
    seed: int | None = 42,
) -> pd.DataFrame:
    """
    Simulate synthetic market data with OHLCV columns.
    Prices are generated from log returns using a drift + noise model.
    Volume is generated around a baseline with noise and occasional spikes.
    """
    if n_days < 50:
        raise ValueError("Use at least 50 days so indicators have time to settle.")

    mu, sigma = get_regime_params(regime)

    rng = np.random.default_rng(seed)

    # log returns and closes
    eps = rng.normal(0.0, 1.0, n_days)
    log_returns = mu + sigma * eps

    closes = np.empty(n_days)
    closes[0] = start_price
    for t in range(1, n_days):
        closes[t] = closes[t - 1] * np.exp(log_returns[t])

    # simple OHLC construction around close
    opens = np.empty(n_days)
    highs = np.empty(n_days)
    lows = np.empty(n_days)

    opens[0] = start_price
    intraday_scale = max(0.003, sigma * 0.8)

    for t in range(n_days):
        if t > 0:
            opens[t] = closes[t - 1]

        intraday_up = abs(rng.normal(0.0, intraday_scale))
        intraday_down = abs(rng.normal(0.0, intraday_scale))

        highs[t] = max(opens[t], closes[t]) * (1.0 + intraday_up)
        lows[t] = min(opens[t], closes[t]) * max(0.001, 1.0 - intraday_down)

    # volume with noise and spikes
    vol_noise = rng.normal(0.0, 0.15, n_days)
    spike_flags = rng.random(n_days) < 0.08
    spike_sizes = rng.uniform(1.5, 3.0, n_days)

    volumes = base_volume * (1.0 + vol_noise)
    volumes = np.maximum(volumes, base_volume * 0.2)
    volumes = np.where(spike_flags, volumes * spike_sizes, volumes)

    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n_days, freq="B")

    df = pd.DataFrame(
        {
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes.astype(int),
            "LogReturn": log_returns,
        },
        index=dates,
    )
    return df
