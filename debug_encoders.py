import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

def debug_encoders():
    dataset_path = 'backend/dataset/career_prediction_dataset.csv'
    df = pd.read_csv(dataset_path)
    
    categorical_cols = ['Degree', 'Specialization', 'College_Name']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = df[col].astype(str).str.strip()
        le.fit(df[col])
        print(f"\n--- {col} Classes ---")
        print(f"Index 0: {le.classes_[0]}")
        print(f"Index 1: {le.classes_[1]}")
        print(f"Total Classes: {len(le.classes_)}")
        
        # Check if 'Electronics' is in there
        matches = [c for c in le.classes_ if 'electronics' in c.lower()]
        print(f"Classes matching 'electronics': {matches}")
        
        # Check 'CSE'
        matches_cse = [c for c in le.classes_ if 'cse' in c.lower() or 'computer' in c.lower()]
        print(f"Classes matching 'cse/computer': {matches_cse}")

if __name__ == "__main__":
    debug_encoders()
