import logging

import pandas as pd


class Transformer:
    def __init__(self):
        self.DROP_COLUMNS = [

        ]
        self.ONE_HOT_ENCODE_COLUMNS = [
            "marital",
            "job",
            "education",
            "poutcome",
            "housing",
            "loan",
            "contact"
        ]
        self.BINARY_FEATURES = [
            "housing",
            "loan",
            "default",
            "y"
        ]

    def transform(self) -> pd.DataFrame:

        df = pd.read_parquet("temp/dataset.parquet")
        df = df.drop(self.DROP_COLUMNS, axis=1)
        df = self._map_binary_column_to_int(df)
        df = self._map_month_to_int(df)
        df = self._one_hot_encode_columns(df)
        df = self._pdays_from_int_to_categories(df)

        logging.info('Starting to write data locally')
        df.to_parquet("temp/dataset-transformed.parquet")
        logging.info('Data stored locally')

    def _map_binary_column_to_int(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('Mapping binary columns to integers')
        for col in self.BINARY_FEATURES:
            df[col] = df[col].map({'yes': 1, 'no': 0})
        return df


    def _map_month_to_int(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('Mapping month column to integers')
        month_mapping = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        df["month"] = df["month"].map(month_mapping)

        return df

    def _one_hot_encode_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('One-hot encoding categorical columns')
        df = pd.get_dummies(df, columns=self.ONE_HOT_ENCODE_COLUMNS, drop_first=True)
        return df

    def _pdays_from_int_to_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('Transforming pdays column to categories')
        return df
    
def transform_data():
    import logging
    logging.info('Starting transform_data')
    
    transformer = Transformer()  # Instantiate your class
    transformer.transform()  # Call the transform method
    
    logging.info('Data transformation completed')