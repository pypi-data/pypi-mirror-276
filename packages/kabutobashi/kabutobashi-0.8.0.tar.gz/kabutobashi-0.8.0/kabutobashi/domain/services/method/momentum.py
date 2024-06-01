import pandas as pd

from .method import Method, MethodType, ProcessMethod, VisualizeMethod


class MomentumProcess(ProcessMethod):
    """
    See Also:
        https://www.sevendata.co.jp/shihyou/technical/momentum.html
    """

    term: int = 25
    method_name: str = "momentum"
    method_type: MethodType = MethodType.TECHNICAL_ANALYSIS

    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.assign(
            momentum=df["close"].shift(10),
        ).fillna(0)
        df = df.assign(sma_momentum=lambda x: x["momentum"].rolling(self.term).mean())
        return df

    def _signal(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.join(self._cross(df["sma_momentum"]))
        df = df.rename(columns={"to_plus": "buy_signal", "to_minus": "sell_signal"})
        return df

    def _processed_columns(self) -> list:
        return ["momentum", "sma_momentum"]

    def _parameterize(self, df_x: pd.DataFrame, df_p: pd.DataFrame) -> dict:
        return {}


class MomentumVisualize(VisualizeMethod):
    """
    See Also:
        https://www.sevendata.co.jp/shihyou/technical/momentum.html
    """

    def _color_mapping(self) -> list:
        return [
            {"df_key": "momentum", "color": "", "label": "momentum"},
            {"df_key": "sma_momentum", "color": "", "label": "sma_momentum"},
        ]

    def _visualize_option(self) -> dict:
        return {"position": "lower"}


momentum = Method.of(process_method=MomentumProcess(), visualize_method=MomentumVisualize())
