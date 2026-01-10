import pandas as pd
import os
from users.ml import CareerPredictor
import sys

# Setup Django standalone (needed for some imports potentially, though ml.py seems independent-ish)
# Actually ml.py uses settings for paths maybe? Let's check imports.
# ml.py uses os only.

def clean_and_retrain():
    dataset_path = 'backend/dataset/career_prediction_dataset.csv'
    
    print(f"Reading {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    initial_count = len(df)
    print(f"Initial row count: {initial_count}")
    
    # Filter out 'good'
    df_clean = df[df['Job_Role'].str.lower() != 'good']
    
    final_count = len(df_clean)
    print(f"Final row count: {final_count}")
    print(f"Removed {initial_count - final_count} rows.")
    
    # Save back
    df_clean.to_csv(dataset_path, index=False)
    print("Saved cleaned dataset.")
    
    # Retrain
    print("Retraining model...")
    predictor = CareerPredictor()
    metrics = predictor.train_model()
    print("Training complete.")
    print("Metrics:", metrics)

if __name__ == "__main__":
    clean_and_retrain()
