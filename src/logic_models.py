import pandas as pd


def evaluate_naive(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["B0"] = (out["P"] & out["M"] & out["D"]) | (out["R"] & out["V"])
    out["S0"] = ((~out["P"]) & (~out["M"]) & (~out["D"])) | (out["O"] & out["V"])
    out["H0"] = (~out["B0"]) & (~out["S0"])
    out["Conflict0"] = out["B0"] & out["S0"]

    return out


def evaluate_refined(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["B1"] = (((out["P"] & out["M"] & out["D"]) | (out["R"] & out["V"])) & (~out["O"]))
    out["S1"] = ((((~out["P"]) & (~out["M"]) & (~out["D"])) | (out["O"] & out["V"])) & (~out["R"]))
    out["H1"] = (~out["B1"]) & (~out["S1"])
    out["Conflict1"] = out["B1"] & out["S1"]

    return out


def summarize_outputs(df: pd.DataFrame) -> dict[str, int]:
    return {
        "B0_buy_count": int(df["B0"].sum()),
        "S0_sell_count": int(df["S0"].sum()),
        "H0_hold_count": int(df["H0"].sum()),
        "Conflict0_count": int(df["Conflict0"].sum()),
        "B1_buy_count": int(df["B1"].sum()),
        "S1_sell_count": int(df["S1"].sum()),
        "H1_hold_count": int(df["H1"].sum()),
        "Conflict1_count": int(df["Conflict1"].sum()),
    }
