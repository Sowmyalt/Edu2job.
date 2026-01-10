import sys
import os
import json

# Ensure users module can be found
sys.path.append(os.getcwd())

from users.ml import CareerPredictor

def verify_fix():
    print("Initializing Predictor (this trains the model)...")
    predictor = CareerPredictor()
    
    test_cases = [
        # Case 1: Electronics (Should map to ECE)
        {
            "profile": {
                "Degree": "B.Tech",
                "Specialization": "Electronics", 
                "College_Name": "IIT",
                "CGPA": "8.5",
                "Graduation_Year": 2024
            },
            "description": "Electronics Input"
        },
        # Case 2: CSE (Should map to Computer Science...)
        {
            "profile": {
                "Degree": "B.Tech",
                "Specialization": "CSE",
                "College_Name": "IIT",
                "CGPA": "8.5",
                "Graduation_Year": 2024
            },
            "description": "CSE Input"
        },
        # Case 3: Electrical (Map to EEE)
        {
             "profile": {
                "Degree": "B.Tech",
                "Specialization": "Electrical",
                "College_Name": "IIT",
                 "CGPA": "8.5",
                "Graduation_Year": 2024
             },
             "description": "Electrical Input"
        }
    ]
    
    for case in test_cases:
        print(f"\n--- Testing {case['description']} ---")
        preds = predictor.predict(case['profile'])
        top_role = preds[0]['role']
        print(f"Top Prediction: {top_role}")
        print(f"Confidence: {preds[0]['confidence']}")
        print(f"All Predictions: {[p['role'] for p in preds]}")

if __name__ == "__main__":
    verify_fix()
