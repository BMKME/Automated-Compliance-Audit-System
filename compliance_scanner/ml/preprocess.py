# compliance_scanner/ml/preprocess.py
import pandas as pd

def preprocess_dataset(filepath):
    data = pd.read_csv(filepath)
    # Perform preprocessing like cleaning, feature extraction, etc.
    return data
