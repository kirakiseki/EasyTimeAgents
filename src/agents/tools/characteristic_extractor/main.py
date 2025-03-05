import pandas as pd


class CharacteristicExtractResult:
    # 相关性、过渡、转移、季节性、趋势、平稳性
    Correlation: float
    Transition: float
    Shifting: float
    Seasonality: float
    Trend: float
    Stationarity: float

    def __init__(self, data: dict):
        self.Correlation = data.get("Correlation", None)
        self.Transition = data.get("Transition", None)
        self.Shifting = data.get("Shifting", None)
        self.Seasonality = data.get("Seasonality", None)
        self.Trend = data.get("Trend", None)
        self.Stationarity = data.get("Stationarity", None)

    def __str__(self) -> str:
        return f"""
Correlation（相关性）: {self.Correlation}
Transition（过渡）: {self.Transition}
Shifting（转移）: {self.Shifting}
Seasonality（季节性）: {self.Seasonality}
Trend（趋势）: {self.Trend}
Stationarity（平稳性）: {self.Stationarity}
"""


def characteristic_extractor(data_path: str) -> CharacteristicExtractResult:

    dummy = "upload/dummy_chars_etth1_tfb.csv"
    df = pd.read_csv(dummy)  # shape: 1x6

    return CharacteristicExtractResult(
        {
            "Correlation": df["Correlation"].values[0],
            "Transition": df["Transition"].values[0],
            "Shifting": df["Shifting"].values[0],
            "Seasonality": df["Seasonality"].values[0],
            "Trend": df["Trend"].values[0],
            "Stationarity": df["Stationarity"].values[0],
        }
    )
