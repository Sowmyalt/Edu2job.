import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

class CareerPredictor:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.target_encoder = LabelEncoder()
        # Initialize and train on import/instantiation for now
        # In production, you'd load a saved model
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'career_prediction_dataset.csv')
        self.train_model()

    def train_model(self):
        try:
            if not os.path.exists(self.dataset_path):
                print(f"Dataset not found at {self.dataset_path}")
                return

            df = pd.read_csv(self.dataset_path)
            
            # Preprocessing
            # 1. CGPA Parsing
            df['CGPA_Float'] = df['CGPA'].apply(self._parse_cgpa)
            
            # 2. Encoders
            self.label_encoders = {}
            categorical_cols = ['Degree', 'Specialization', 'College_Name'] # Ignoring College_Type for now as we don't capture it
            
            for col in categorical_cols:
                le = LabelEncoder()
                # Handle potential unknown values by appending 'Other' explicitly if needed, 
                # but for training we just fit on what we have.
                df[col] = df[col].astype(str).str.strip()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
            
            # Target
            self.target_encoder = LabelEncoder()
            y = self.target_encoder.fit_transform(df['Job_Role'])
            
            # Features
            # Using: Degree, Specialization, College_Name, CGPA_Float, Certificates, Graduation_Year
            X = df[['Degree', 'Specialization', 'College_Name', 'CGPA_Float', 'Certificates', 'Graduation_Year']]
            
            # Train Random Forest
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            print("Model trained successfully on CSV dataset.")
            
        except Exception as e:
            print(f"Error training model: {e}")

    def _parse_cgpa(self, val):
        if isinstance(val, (int, float)):
            return float(val)
        val = str(val).strip()
        if "–" in val or "-" in val:
            parts = val.replace('–', '-').split('-')
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return float(parts[0])
        if "Below" in val:
            return 5.5
        try:
            return float(val)
        except:
            return 7.5

    def _get_encoded_value(self, col, val):
        le = self.label_encoders.get(col)
        if not le:
            return 0
        
        val_str = str(val).strip()
        
        # 1. Try exact match
        try:
            return le.transform([val_str])[0]
        except ValueError:
            pass

        # 2. explicit keyword mapping (Normalize input to lower for check)
        val_lower = val_str.lower()
        mapping = {}
        
        if col == 'Specialization':
            mapping = {
                'electronics': 'ECE',
                'ece': 'ECE',
                'eee': 'EEE',
                'electrical': 'EEE',
                'cse': 'Computer Science and Engineering (CSE)',
                'computer science': 'Computer Science and Engineering (CSE)',
                'cs': 'CS',
                'it': 'Information Technology (IT)',
                'information technology': 'Information Technology (IT)',
                'civil': 'Civil Engineering',
                'mech': 'Mechanical Engineering',
                'mechanical': 'Mechanical Engineering',
                'bio': 'Biotechnology',
                'ai': 'Artificial Intelligence',
                'ml': 'Artificial Intelligence',
                'data': 'Data Science'
            }
        elif col == 'Degree':
            mapping = {
                'b.tech': 'B.Tech',
                'btech': 'B.Tech',
                'be': 'B.E',
                'm.tech': 'M.Tech',
                'mtech': 'M.Tech',
                'bca': 'BCA',
                'mca': 'MCA',
                'bsc': 'B.Sc',
                'msc': 'M.Sc'
            }

        # Check mapping
        for key, target in mapping.items():
            if key in val_lower: # Basic containment check
                try:
                    return le.transform([target])[0]
                except ValueError:
                    continue # Target might not exist in this specific encoder version?

        # 3. Fuzzy match / Fallback to 'Other'
        # Check if 'Other' is a valid class
        try:
            return le.transform(['Other'])[0]
        except ValueError:
            # If 'Other' doesn't exist, finding the most frequent class or just 0 is fallback.
            # But 0 (Architecture) is bad.
            # Let's try to return the code for the most generic class if we can find it.
            # Since we can't easily identify it, we stick to 0 but warn.
            # Better: use fuzzy matching with difflib
            pass
            
        import difflib
        matches = difflib.get_close_matches(val_str, le.classes_, n=1, cutoff=0.6)
        if matches:
             return le.transform([matches[0]])[0]

        return 0

    def predict(self, user_profile):
        """
        user_profile expects keys: 'Degree', 'Specialization', 'College_Name', 'CGPA', 'Certificates', 'Graduation_Year'
        """
        try:
            if not self.model:
                return "Model not trained"

            # Extract raw inputs
            degree = user_profile.get('Degree', 'Other')
            spec = user_profile.get('Specialization', 'Other')
            college = user_profile.get('College_Name', 'Other')
            cgpa_raw = user_profile.get('CGPA', '7.0-7.9')
            certs = int(user_profile.get('Certificates', 0))
            year = int(user_profile.get('Graduation_Year', 2024))
            
            # Preprocess
            cgpa_float = self._parse_cgpa(cgpa_raw)
            degree_enc = self._get_encoded_value('Degree', degree)
            spec_enc = self._get_encoded_value('Specialization', spec)
            college_enc = self._get_encoded_value('College_Name', college)
            
            # Feature Vector
            # Order must match training: Degree, Specialization, College_Name, CGPA_Float, Certificates, Graduation_Year
            features = np.array([[degree_enc, spec_enc, college_enc, cgpa_float, certs, year]])
            
            # Predict
            # Get probabilities for all classes
            probs = self.model.predict_proba(features)[0]
            
            # Get top 5 predictions
            top_5_indices = np.argsort(probs)[-5:][::-1]
            top_5_classes = self.target_encoder.inverse_transform(top_5_indices)
            top_5_probs = probs[top_5_indices]
            
            from .job_data import JOB_KNOWLEDGE_BASE, DOMAIN_KEYWORDS
            
            detailed_predictions = []
            
            # Rule-Based Check (User Request Hybrid Approach)
            from .domain_rules import get_rule_based_recommendations
            rule_roles = get_rule_based_recommendations(spec)
            
            final_predictions = []
            
            # If rules found, prioritize them
            if rule_roles:
                for idx, role in enumerate(rule_roles):
                     # Fetch description/skills
                    details = JOB_KNOWLEDGE_BASE.get(role, JOB_KNOWLEDGE_BASE["General Specialist"])
                    
                    missing = details['skills']
                    if certs > 2:
                        missing = details['skills'][2:]
                    
                    # High confidence for rules
                    conf = 0.95 - (idx * 0.02)
                    
                    final_predictions.append({
                        "role": role,
                        "confidence": float(f"{conf:.2f}"),
                        "match_score": 98 - idx,
                        "justification": f"Strongly recommended for {spec} background.",
                        "missing_skills": missing,
                        "recommended_certs": details['recommended_certs'],
                        "description": details['description']
                    })
                    
                # Optionally append top 1-2 ML predictions if they are distinct
                # ...
                return final_predictions
            
            # If no rules matched, proceed with ML Logic
            
            # Domain boost logic: Check if user specialization matches a domain
            user_spec_lower = spec.lower()
            boost_roles = []
            for key, roles in DOMAIN_KEYWORDS.items():
                if key.lower() in user_spec_lower:
                    boost_roles = roles
                    break
            
            for rank, (role, prob) in enumerate(zip(top_5_classes, top_5_probs)):
                # Apply boost if applicable and not already high
                # Simplified: Just ensure justification mentions it
                
                details = JOB_KNOWLEDGE_BASE.get(role, JOB_KNOWLEDGE_BASE["General Specialist"])
                
                # Check for skill gaps (Simulation based on generic role skills vs user certs count?)
                # Since we don't have user skills input, we list all role skills as "recommended" 
                # or "missing" if certs < 2
                
                missing = details['skills']
                if certs > 2:
                    missing = details['skills'][2:] # Assume they have basics
                
                justification = []
                match_score = int(prob * 100)
                
                if role in boost_roles:
                    justification.append(f"Strong match with your background in {spec}.")
                    match_score = min(99, match_score + 10) # Boost score display
                elif prob > 0.2:
                    justification.append("Good statistical match based on academic profile.")
                else:
                    justification.append("Potential alternative path.")
                    
                if certs > 0:
                    justification.append(f"Your {certs} certificates boost this profile.")
                
                detailed_predictions.append({
                    "role": role,
                    "confidence": float(f"{prob:.2f}"),
                    "match_score": match_score,
                    "justification": " ".join(justification),
                    "missing_skills": missing,
                    "recommended_certs": details['recommended_certs'],
                    "description": details['description']
                })
            
            return detailed_predictions

            return detailed_predictions
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback
            return [{
                "role": "Software Engineer", # Default safe fallback
                "confidence": 0.0,
                "match_score": 0,
                "justification": "Error in prediction processing.",
                "missing_skills": [],
                "recommended_certs": [],
                "description": "Fallback prediction due to system error."
            }]
