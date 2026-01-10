
# Mapping of (Normalized Degree/Spec Keywords) -> List of Roles

# We will use this dictionary to lookup strict rule-based recommendations.
# The key logic in ml.py will be to fuzzy match the user's input to these keys.

DOMAIN_RULES = {
    "CSE": [
        "Software Developer / Engineer",
        "Data Analyst / Data Scientist",
        "Machine Learning Engineer",
        "Full Stack / Backend Developer",
        "Cybersecurity Analyst"
    ],
    "Computer Science": [ # Alias for CSE
        "Software Developer / Engineer",
        "Data Analyst / Data Scientist",
        "Machine Learning Engineer",
        "Full Stack / Backend Developer",
        "Cybersecurity Analyst"
    ],
    "Information Technology": [
        "Software Engineer",
        "Web Developer",
        "System Analyst",
        "Database Administrator",
        "IT Support / Network Engineer"
    ],
    "IT": [ # Alias
        "Software Engineer",
        "Web Developer",
        "System Analyst",
        "Database Administrator",
        "IT Support / Network Engineer"
    ],
    "AI & ML": [
        "Machine Learning Engineer",
        "AI Research Engineer",
        "Data Scientist",
        "Computer Vision Engineer",
        "NLP Engineer"
    ],
    "Artificial Intelligence": [
        "Machine Learning Engineer",
        "AI Research Engineer",
        "Data Scientist",
        "Computer Vision Engineer",
        "NLP Engineer"
    ],
    "Data Science": [
        "Data Analyst",
        "Data Scientist",
        "Business Intelligence Engineer",
        "Data Engineer",
        "Analytics Consultant"
    ],
    "Cyber Security": [
        "Cybersecurity Analyst",
        "Ethical Hacker",
        "Security Engineer",
        "SOC Analyst",
        "Digital Forensics Analyst"
    ],
    "Mechanical": [
        "Mechanical Design Engineer",
        "Production / Manufacturing Engineer",
        "Automotive Engineer",
        "Maintenance Engineer",
        "Quality Control Engineer"
    ],
    "Electrical": [
        "Electrical Design Engineer",
        "Power Systems Engineer",
        "Control Systems Engineer",
        "Electrical Maintenance Engineer",
        "Renewable Energy Engineer"
    ],
    "EEE": [
        "Electrical Design Engineer",
        "Power Systems Engineer",
        "Control Systems Engineer",
        "Electrical Maintenance Engineer",
        "Renewable Energy Engineer"
    ],
    "Electronics": [
        "Embedded Systems Engineer",
        "VLSI Design Engineer",
        "Electronics Hardware Engineer",
        "Communication Engineer",
        "IoT Engineer"
    ],
    "ECE": [
        "Embedded Systems Engineer",
        "VLSI Design Engineer",
        "Electronics Hardware Engineer",
        "Communication Engineer",
        "IoT Engineer"
    ],
    "Instrumentation": [
        "Instrumentation Engineer",
        "Control Systems Engineer",
        "Automation Engineer",
        "Process Control Engineer",
        "Calibration Engineer"
    ],
    "EIE": [
         "Instrumentation Engineer",
        "Control Systems Engineer",
        "Automation Engineer",
        "Process Control Engineer",
        "Calibration Engineer"
    ],
    "Civil": [
        "Site Engineer",
        "Structural Engineer",
        "Project Manager",
        "Construction Planner",
        "Quantity Surveyor"
    ],
    "Chemical": [
        "Process Engineer",
        "Production Engineer",
        "Chemical Plant Operations Engineer",
        "Quality Control Engineer",
        "Safety Engineer"
    ],
    "Metallurgical": [
        "Metallurgical Engineer",
        "Quality Assurance Engineer",
        "Materials Engineer",
        "Production Engineer",
        "Failure Analysis Engineer"
    ],
    "Aerospace": [
        "Aerospace Design Engineer",
        "Aircraft Maintenance Engineer",
        "Avionics Engineer",
        "Flight Systems Engineer",
        "Defense Research Engineer"
    ],
    "Biotechnology": [
        "Biotechnologist",
        "Research Scientist",
        "Clinical Data Analyst",
        "Bioprocess Engineer",
        "Quality Control Analyst"
    ],
    "Biomedical": [
        "Biomedical Equipment Engineer",
        "Medical Device Engineer",
        "Clinical Engineer",
        "Healthcare Technology Analyst",
        "Imaging Systems Engineer"
    ],
    "Mechatronics": [
        "Robotics Engineer",
        "Automation Engineer",
        "Control Systems Engineer",
        "Embedded Engineer",
        "Industrial Design Engineer"
    ],
    "Environmental": [
        "Environmental Engineer",
        "Sustainability Analyst",
        "Water Resources Engineer",
        "Waste Management Engineer",
        "Environmental Consultant"
    ],
    "Agricultural": [
        "Agricultural Engineer",
        "Farm Machinery Engineer",
        "Irrigation Engineer",
        "Agri-Tech Analyst",
        "Precision Agriculture Specialist"
    ],
    "Robotics": [
        "Robotics Engineer",
        "Automation Engineer",
        "Embedded Systems Engineer",
        "AI Robotics Engineer",
        "Control Systems Engineer"
    ],
    "IoT": [
        "IoT Developer",
        "Embedded Engineer",
        "Smart Systems Engineer",
        "Industrial IoT Engineer",
        "Sensor Network Engineer"
    ],
    "Internet of Things": [
        "IoT Developer",
        "Embedded Engineer",
        "Smart Systems Engineer",
        "Industrial IoT Engineer",
        "Sensor Network Engineer"
    ],
    "Cloud Computing": [
        "Cloud Engineer",
        "DevOps Engineer",
        "Site Reliability Engineer (SRE)",
        "Cloud Security Engineer",
        "Solutions Architect"
    ],
     "Cloud": [
        "Cloud Engineer",
        "DevOps Engineer",
        "Site Reliability Engineer (SRE)",
        "Cloud Security Engineer",
        "Solutions Architect"
    ]
}

def get_rule_based_recommendations(specialization):
    """
    Returns a list of roles if the specialization matches a known key.
    Case-insensitive matching.
    """
    if not specialization:
        return []
    
    spec_norm = specialization.lower().strip()
    
    # 1. Direct key match (insensitive)
    for key, roles in DOMAIN_RULES.items():
        if key.lower() == spec_norm:
            return roles
            
    # 2. Contains match (e.g., "Computer Science" in "B.Tech Computer Science")
    # Priority to longer keys to match "Computer Science" over "Computer" if we had it
    sorted_keys = sorted(DOMAIN_RULES.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        if key.lower() in spec_norm:
            return DOMAIN_RULES[key]
            
    return []
