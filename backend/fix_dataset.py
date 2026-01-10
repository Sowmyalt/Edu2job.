import pandas as pd
import os
import sys

# Ensure we can import from users app
sys.path.append(os.getcwd())

from users.ml import CareerPredictor

def clean_and_retrain():
    # Path relative to backend/ (where this script resides)
    dataset_path = os.path.join(os.getcwd(), 'dataset', 'career_prediction_dataset.csv')
    
    print(f"Reading {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    initial_count = len(df)
    print(f"Initial row count: {initial_count}")
    
    # Filter out 'good' (case insensitive)
    # Also drop any rows where Job_Role is null/empty just in case
    df_clean = df[df['Job_Role'].notna()]
    df_clean = df_clean[df_clean['Job_Role'].str.lower() != 'good']
    
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
