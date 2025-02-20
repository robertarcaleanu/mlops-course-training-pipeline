import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split
from transform import Transformer


class RandomForestTrainer:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.transformer = Transformer()

    def preprocess_data(self, df: pd.DataFrame, target_column: str):
        df = self.transformer.transform(df)

    def train(self, df: pd.DataFrame, target_column: str, test_size: float = 0.2):
        # Preprocess the data
        X, y = self.preprocess_data(df, target_column)

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=self.random_state)
        self.model = RandomForestClassifier(random_state=self.random_state)


        # Define the parameter grid for Grid Search
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['auto', 'sqrt', 'log2']
        }

        # Perform Grid Search with Cross Validation
        grid_search = GridSearchCV(estimator=self.model, param_grid=param_grid, 
                                   cv=5, n_jobs=-1, scoring='accuracy')

        # Fit the Grid Search model
        grid_search.fit(X_train, y_train)

        # Best parameters from Grid Search
        print("Best Parameters from Grid Search:", grid_search.best_params_)

        # Train the best model found by Grid Search
        self.model = grid_search.best_estimator
        