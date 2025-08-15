import os
from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd

def train_model():
    # Path to the dataset
    dataset_path = 'compliance_scanner/ml/datasets/training_data.csv'
    
    # Ensure the dataset exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    # Load the dataset
    print("Loading dataset...")
    data = pd.read_csv(dataset_path)

    # Check dataset structure
    print(f"Dataset loaded. Shape: {data.shape}")

    # Train the Isolation Forest model
    print("Training model...")
    model = IsolationForest()
    model.fit(data)

    # Path to save the model
    model_path = 'compliance_scanner/ml/model.pkl'
    
    # Save the trained model
    print("Saving model...")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
