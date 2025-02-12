import pandas as pd


class Transformer:
    def __init__(self):
        self.DROP_COLUMNS = [
            
        ]

    def transform(self, df: pd.DataFrame, balance_is_required: bool = True) -> pd.DataFrame:
        df = df.drop(self.DROP_COLUMNS, axis=1)
        if balance_is_required:
            df = self._balance_dataset(df)
        df = self._map_target_to_int(df)
        df = self._pdays_from_int_to_categories(df)

    def _map_target_to_int(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _balance_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _pdays_from_int_to_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
