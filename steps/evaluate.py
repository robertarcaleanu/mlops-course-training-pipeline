import os

import boto3
import joblib
from sklearn.metrics import accuracy_score


class ModelEvaluator:
    def __init__(self, model, s3_bucket: str, s3_key_prefix: str = 'models/', threshold: float = 0.9):

        self.model = model
        self.s3_bucket = s3_bucket
        self.s3_key_prefix = s3_key_prefix
        self.threshold = threshold
        self.s3_client = boto3.client('s3')

    def evaluate(self, X_test, y_test):
        # Predict with the trained model
        y_pred = self.model.predict(X_test)

        # Calculate accuracy for classification
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")

        # If the model performs better than the threshold, save to S3
        if accuracy > self.threshold:
            print(f"Accuracy is above the threshold of {self.threshold}. Saving model to S3...")
            self.save_model_to_s3()
            return accuracy

        return None

    def save_model_to_s3(self):

        model_filename = 'model.pkl'

        # Save the model locally first
        joblib.dump(self.model, model_filename)

        # Upload the model to the specified S3 bucket
        try:
            s3_key = os.path.join(self.s3_key_prefix, model_filename)
            self.s3_client.upload_file(model_filename, self.s3_bucket, s3_key)
            print(f"Model saved successfully to s3://{self.s3_bucket}/{s3_key}")
        except Exception as e:
            print(f"Error saving the model to S3: {str(e)}")
        finally:
            # Optionally remove the local file after upload
            if os.path.exists(model_filename):
                os.remove(model_filename)
