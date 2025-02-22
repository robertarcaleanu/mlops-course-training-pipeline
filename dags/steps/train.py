def train_model():
    import logging

    import joblib
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OneHotEncoder
    
    logging.info("Starting model training")

    class RandomForestTrainer:
        def __init__(self, random_state: int = 42):
            self.random_state = random_state
            self.ONE_HOT_ENCODE_COLUMNS = [
                "marital",
                "job",
                "education",
                "poutcome",
                "contact"
                ]
        
        def _one_hot_encode_columns(self, df: pd.DataFrame) -> pd.DataFrame:
            logging.info('One-hot encoding categorical columns using sklearn OneHotEncoder')

            # Create an encoder for the categorical columns
            encoder = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore').set_output(transform="pandas")
            
            # Fit the encoder and transform the data
            encoded_df = encoder.fit_transform(df[self.ONE_HOT_ENCODE_COLUMNS])

            logging.info("Saving encoder")
            joblib.dump(encoder, 'temp/one_hot_encoder.joblib')
            
            # Drop the original categorical columns and concatenate the encoded columns
            df = df.drop(columns=self.ONE_HOT_ENCODE_COLUMNS)
            df = pd.concat([df, encoded_df], axis=1)
            
            return df


        def _preprocess_data(self, target_column: str):
            df = pd.read_parquet("temp/dataset-transformed.parquet")
            df = self._one_hot_encode_columns(df)
            X = df.drop(target_column, axis=1)
            y = df[target_column]
            return X, y

        def train(self, target_column: str = 'y', test_size: float = 0.3):
            # Preprocess the data
            logging.info("Preprocessing data")
            X, y = self._preprocess_data(target_column)

            # Split into training and testing sets
            logging.info("Splitting data into training and testing sets")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=self.random_state)

            # Initialize the model here
            logging.info("Training the RandomForest model")
            model = RandomForestClassifier(random_state=self.random_state)
            model.fit(X_train, y_train)

            logging.info("Saving the trained model")

            joblib.dump(model, "temp/model.joblib")
        
    # Create an instance of the RandomForestTrainer class and call the train method
    rf_trainer = RandomForestTrainer()
    rf_trainer.train()
    
    logging.info("Model training completed")



