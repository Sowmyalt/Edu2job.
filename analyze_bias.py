import pandas as pd
import os

def analyze_dataset():
    dataset_path = 'backend/dataset/career_prediction_dataset.csv'
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    df = pd.read_csv(dataset_path)
    
    print("\n--- 'Electronics' Analysis ---")
    electronics_mask = df['Specialization'].str.contains('Electronics', case=False, na=False) | \
                       df['Degree'].str.contains('Electronics', case=False, na=False) | \
                       df['Specialization'].str.contains('ECE', case=False, na=False)
    electronics_df = df[electronics_mask]
    print(f"Total 'Electronics/ECE' rows: {len(electronics_df)}")
    print(electronics_df['Job_Role'].value_counts())
    
    print("\n--- 'CSE' Analysis ---")
    cse_mask = df['Specialization'].str.contains('CSE', case=False, na=False) | \
               df['Degree'].str.contains('CSE', case=False, na=False) | \
               df['Specialization'].str.contains('Computer Science', case=False, na=False)
    cse_df = df[cse_mask]
    print(f"Total 'CSE' rows: {len(cse_df)}")
    print(cse_df['Job_Role'].value_counts())

if __name__ == "__main__":
    analyze_dataset()
