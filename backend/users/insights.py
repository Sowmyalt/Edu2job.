import pandas as pd
import os
from collections import Counter

class CareerInsights:
    def __init__(self):
        self.dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'career_prediction_dataset.csv')
        self.df = None
        self._load_data()

    def _load_data(self):
        try:
            if os.path.exists(self.dataset_path):
                self.df = pd.read_csv(self.dataset_path)
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def get_role_distribution(self):
        """Returns top 10 job roles count."""
        if self.df is None: return []
        
        counts = self.df['Job_Role'].value_counts().head(10)
        return [{"name": role, "value": int(count)} for role, count in counts.items()]

    def get_degree_trends(self, degree_filter=None):
        """Returns role distribution grouped by Degree (Top 3 roles per degree)."""
        if self.df is None: return []

        data = []
        if degree_filter:
            # Case insensitive partial match (e.g., "B.Tech" matches "B.Tech/B.E.")
            # Normalizing to lower for check
            # Filter df first
            # Safe checking
            filtered_df = self.df[self.df['Degree'].astype(str).str.contains(degree_filter, case=False, na=False)]
            if filtered_df.empty:
               # If strict match fails, try finding unique degrees and see if any fuzzy match
               # For now, fallback to all or return empty?
               # Let's return all degrees but put the matched one first? 
               # Or just return all if filter yields nothing.
               degrees = self.df['Degree'].unique()
            else:
               degrees = filtered_df['Degree'].unique()
        else:
            degrees = self.df['Degree'].unique()
        
        for deg in degrees:
            if degree_filter:
                 subset = self.df[self.df['Degree'] == deg] # Use original df subset by this specific degree found
            else:
                 subset = self.df[self.df['Degree'] == deg]
                 
            top_roles = subset['Job_Role'].value_counts().head(3)
            
            roles_data = [{"role": r, "count": int(c)} for r, c in top_roles.items()]
            data.append({
                "degree": deg,
                "top_roles": roles_data
            })
            
        return data

    def get_specialization_insights(self, specialization_filter=None):
        """Returns role distribution for a specific specialization."""
        if self.df is None: return []
        
        if specialization_filter:
            subset = self.df[self.df['Specialization'] == specialization_filter]
        else:
            subset = self.df
            
        counts = subset['Job_Role'].value_counts().head(5)
        return [{"name": role, "value": int(count)} for role, count in counts.items()]
    def get_personalized_insights(self, profile):
        """
        Generates 5-section personalized market data.
        """
        try:
            from .utils.jsearch import JSearchClient
            client = JSearchClient()
            
            # 1. Extract User Context
            edu = profile.get('academic_info', {}).get('education', [{}])[0]
            specialization = edu.get('specialization', 'General').strip()
            degree = edu.get('degree', 'Degree').strip()
            # Default location if not in profile
            location = "India" 

            search_query = f"{specialization} {degree} freshers"
            
            # 2. Fetch Live Data (or None)
            live_stats = client.estimate_market_stats(search_query, location)
            
            # 3. Construct Sections using Live Data + Heuristics
            
            # --- Section 1: Market Overview (Trend) ---
            # If live data exists, structure trend around the real job count
            base_demand = live_stats['sample_size'] * 50 if live_stats else 1200 # Multiplier to estimate total market
            trend_data = self._generate_trend(base_demand, specialization)

            # --- Section 2: Where You Stand (Comparison) ---
            # Use Live Salary if available, else Mock
            user_salary = live_stats['avg_salary'] if live_stats and live_stats['avg_salary'] > 0 else 450000
            comparison_data = self._generate_comparison(specialization, user_salary)

            # --- Section 3: Career Paths ---
            # ALWAYS use curated Career Constants for strategic advice. 
            # Live data is too messy (e.g. "Hiring Freshers") for this section.
            career_paths = self._get_mock_career_paths(specialization)

            # --- Section 4: Skill Gap ---
            # Hardcoded skill maps for reliability until we have skill extraction API
            # Extract skills from academic_info
            user_skills = profile.get('academic_info', {}).get('skills', [])
            skill_gap = self._generate_skill_gap(specialization, user_skills)

            # --- Section 5: Future Outlook ---
            outlook = self._generate_outlook(specialization, trend_data)

            return {
                "context": {"specialization": specialization, "degree": degree},
                "market_overview": trend_data,
                "comparison": comparison_data,
                "career_paths": career_paths,
                "skill_gap": skill_gap,
                "future_outlook": outlook
            }

        except Exception as e:
            print(f"Personalization Error: {e}")
            return self._get_fallback_insights()

    def _generate_trend(self, current_demand, specialization):
        # Simulate 5 years: -2, -1, Current, +1, +2
        current_year = 2026
        # Tech/CSE grows faster
        growth_rate = 1.15 if any(x in specialization.lower() for x in ['computer', 'software', 'it', 'data']) else 1.05
        
        data = []
        val = current_demand / (growth_rate ** 2)
        for i in range(-2, 3):
            data.append({
                "year": current_year + i,
                "demand": int(val),
                "growth": "Rising" if growth_rate > 1 else "Stable"
            })
            val *= growth_rate
        return data

    def _generate_comparison(self, user_spec, user_salary):
        # Dynamic Comparison Fields based on Domain
        RELATED_FIELDS = {
            "computer": [
                {"name": "Data Science", "salary_mult": 1.3, "demand": 90},
                {"name": "Electronics", "salary_mult": 0.85, "demand": 65}
            ],
            "software": "computer",
            "it": "computer",
            "data": "computer",

            "electronics": [
                {"name": "Computer Science", "salary_mult": 1.2, "demand": 95},
                {"name": "Electrical Eng", "salary_mult": 0.9, "demand": 60}
            ],
            "ece": "electronics",
            "communication": "electronics",

            "electrical": [
                {"name": "Electronics", "salary_mult": 1.1, "demand": 75},
                {"name": "Civil Eng", "salary_mult": 0.8, "demand": 50}
            ],
            "eee": "electrical",

            "mechanical": [
                {"name": "Robotics", "salary_mult": 1.25, "demand": 80},
                {"name": "Civil Eng", "salary_mult": 0.95, "demand": 55}
            ],

            "civil": [
                {"name": "Architecture", "salary_mult": 1.1, "demand": 60},
                {"name": "Mechanical Eng", "salary_mult": 1.05, "demand": 65}
            ],

            "business": [
                {"name": "Finance", "salary_mult": 1.3, "demand": 75},
                {"name": "Marketing", "salary_mult": 0.9, "demand": 85}
            ],
            "management": "business",
            "mba": "business",
            "commerce": "business"
        }

        # 1. Identify Domain
        spec_lower = user_spec.lower()
        matched_category = None
        for key in RELATED_FIELDS:
            if key in spec_lower:
                val = RELATED_FIELDS[key]
                if isinstance(val, str): val = RELATED_FIELDS[val] # Handle alias
                matched_category = val
                break
        
        # 2. Fallback if unknown
        if not matched_category:
            matched_category = [
                {"name": "General Management", "salary_mult": 1.2, "demand": 70},
                {"name": "Core Engineering", "salary_mult": 0.9, "demand": 60}
            ]

        # 3. Construct Peers List
        peers = [{"name": user_spec, "salary": user_salary, "demand": 85, "is_user": True}]
        
        for field in matched_category:
            peers.append({
                "name": field['name'],
                "salary": int(user_salary * field['salary_mult']),
                "demand": field['demand'],
                "is_user": False
            })

        return peers

    
    def _get_domain_knowledge(self, spec):
        spec = spec.lower()
        
        # Knowledge Base for various domains
        knowledge = {
            "computer": {
                "skills": ["Python", "DSA", "React", "Cloud Computing", "SQL"],
                "roles": [
                    {"title": "Software Engineer", "growth": "High Growth"},
                    {"title": "Data Scientist", "growth": "High Growth"},
                    {"title": "DevOps Engineer", "growth": "Rising"}
                ]
            },
            "software": "computer", # Alias
            "data": "computer",
            "it": "computer",
            
            "electronics": {
                "skills": ["Embedded Systems", "Verilog/VHDL", "MATLAB", "IoT", "Circuit Design"],
                "roles": [
                    {"title": "VLSI Engineer", "growth": "High Growth"},
                    {"title": "Embedded Developer", "growth": "Stable"},
                    {"title": "IoT Architect", "growth": "Rising"}
                ]
            },
            "communication": "electronics",
            "ece": "electronics",
            
            "electrical": {
                "skills": ["Power Systems", "PLC/SCADA", "MATLAB", "Electrical Design", "Control Systems"],
                "roles": [
                    {"title": "Power Engineer", "growth": "Stable"},
                    {"title": "Control Systems Engineer", "growth": "Rising"},
                    {"title": "Automation Specialist", "growth": "High Growth"}
                ]
            },
            "eee": "electrical",
            
            "mechanical": {
                "skills": ["AutoCAD", "SolidWorks", "ANSYS", "Robotics", "Thermodynamics"],
                "roles": [
                    {"title": "Robotics Engineer", "growth": "High Growth"},
                    {"title": "Design Engineer", "growth": "Stable"},
                    {"title": "R&D Engineer", "growth": "Rising"}
                ]
            },
            
            "civil": {
                "skills": ["AutoCAD", "Revit", "STAAD.Pro", "Structural Analysis", "Project Mgmt"],
                "roles": [
                    {"title": "Structural Engineer", "growth": "Stable"},
                    {"title": "BIM Specialist", "growth": "High Growth"},
                    {"title": "Construction Manager", "growth": "Stable"}
                ]
            },
            
            "business": {
                "skills": ["Financial Analysis", "Excel", "Marketing Strategy", "Data Analytics", "CRM"],
                "roles": [
                    {"title": "Business Analyst", "growth": "High Growth"},
                    {"title": "Product Manager", "growth": "Rising"},
                    {"title": "Marketing Manager", "growth": "Stable"}
                ]
            },
            "commerce": "business",
            "mba": "business",
            "management": "business"
        }
        
        # Match Specialization to Key
        for key in knowledge:
            if key in spec:
                val = knowledge[key]
                if isinstance(val, str): # Handle Alias
                    return knowledge[val]
                return val
                
        # Fallback for General/Unknown
        return {
            "skills": ["Communication", "Problem Solving", "Excel", "Project Management", "Analysis"],
            "roles": [
                {"title": "Associate Trainee", "growth": "Stable"},
                {"title": "Operations Executive", "growth": "Stable"},
                {"title": "Business Analyst", "growth": "Rising"}
            ]
        }

    def _get_mock_career_paths(self, spec):
        from .career_constants import CAREER_PATHS_DB
        
        spec_lower = spec.lower()
        
        # Exact or fuzzy match key
        matched_key = None
        for key in CAREER_PATHS_DB:
            if key in spec_lower:
                matched_key = key
                break
        
        if matched_key:
            entry = CAREER_PATHS_DB[matched_key]
            # Handle string alias
            if isinstance(entry, str):
                entry = CAREER_PATHS_DB[entry]
            
            return entry['paths']
            
        # Fallback for completely unknown
        return [
             {"title": "Associate Trainee", "roles": "Entry Level → Operations", "growth": "Stable"},
             {"title": "Business Analyst", "roles": "Analyst → Consultant", "growth": "Rising"}
        ]

    def _generate_skill_gap(self, spec, user_skills):
        info = self._get_domain_knowledge(spec)
        required = info['skills']
            
        # Check presence (Simple string match)
        data = []
        user_skills_lower = [s.lower() for s in user_skills] if user_skills else []
        
        for req in required:
            req_lower = req.lower()
            # Bidirectional Flexible Matching
            # Match if 'React' in 'ReactJS' OR 'Python' in 'Python Programming'
            has_skill = 1 if any((req_lower in us) or (us in req_lower) for us in user_skills_lower) else 0.2
            data.append({"subject": req, "A": 1, "B": has_skill, "fullMark": 1})
            
        return data

    def _generate_outlook(self, spec, trend_data):
        # Simple heuristic
        start = trend_data[0]['demand']
        end = trend_data[-1]['demand']
        direction = "Rising" if end > start else "Stable"
        
        return {
            "verdict": direction,
            "summary": f"The market for {spec} is {direction.lower()} with a projected {(end/start - 1)*100:.1f}% growth over the next 5 years.",
            "impact_factors": ["AI Automation", "Remote Work Shift", "Green Tech"]
        }

    def _get_fallback_insights(self):
        return {
           "error": "Could not generate personalized insights. Using standard view."
        }
