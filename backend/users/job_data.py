JOB_KNOWLEDGE_BASE = {
    # CSE / IT
    "Software Developer": {
        "description": "Designs, codes, and maintains software applications.",
        "skills": ["Java", "Python", "C++", "DSA", "System Design", "Git"],
        "recommended_certs": ["Oracle Certified Master", "AWS Certified Developer"],
        "domains": ["CSE", "IT"]
    },
    "Web Developer": {
        "description": "Builds and maintains websites and web applications.",
        "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "DB Management"],
        "recommended_certs": ["Meta Front-End Developer", "Full Stack Development"],
        "domains": ["CSE", "IT"]
    },
    "Data Scientist": {
        "description": "Analyzes complex data to help make business decisions.",
        "skills": ["Python", "R", "Machine Learning", "Statistics", "SQL"],
        "recommended_certs": ["Google Data Analytics", "IBM Data Science"],
        "domains": ["CSE", "IT", "Data Science"]
    },
    "Machine Learning Engineer": {
        "description": "Designs and builds machine learning systems.",
        "skills": ["Python", "TensorFlow", "PyTorch", "Deep Learning"],
        "recommended_certs": ["AWS Certified Machine Learning", "DeepLearning.AI"],
        "domains": ["CSE", "IT", "AI"]
    },
    "Cloud Engineer": {
        "description": "Designs and manages cloud infrastructure.",
        "skills": ["AWS", "Azure", "Docker", "Kubernetes", "Linux"],
        "recommended_certs": ["AWS Solutions Architect", "Azure Administrator"],
        "domains": ["CSE", "IT"]
    },
    "DevOps Engineer": {
        "description": "Bridges gap between development and operations.",
        "skills": ["CI/CD", "Jenkins", "Docker", "Kubernetes", "Scripting"],
        "recommended_certs": ["Certified Kubernetes Administrator", "DevOps Engineer Expert"],
        "domains": ["CSE", "IT"]
    },
    "Cybersecurity Analyst": {
        "description": "Protects systems and networks from threats.",
        "skills": ["Network Security", "Ethical Hacking", "Cryptography", "Linux"],
        "recommended_certs": ["CompTIA Security+", "CEH"],
        "domains": ["CSE", "IT"]
    },
    
    # ECE
    "Embedded Systems Engineer": {
        "description": "Designs software for embedded devices.",
        "skills": ["C/C++", "Microcontrollers", "RTOS", "Circuit Design"],
        "recommended_certs": ["Arm Accredited Engineer", "Embedded Systems Design"],
        "domains": ["ECE", "EEE"]
    },
    "VLSI Engineer": {
        "description": "Designs integrated circuits.",
        "skills": ["Verilog", "VHDL", "SystemVerilog", "Digital Logic"],
        "recommended_certs": ["VLSI Design", "Physical Design"],
        "domains": ["ECE"]
    },
    "IoT Engineer": {
        "description": "Develops connected devices and systems.",
        "skills": ["IoT Protocols", "Python", "C++", "Cloud Platforms"],
        "recommended_certs": ["Azure IoT Developer", "AWS IoT"],
        "domains": ["ECE", "CSE"]
    },
    
    # ME
    "Mechanical Design Engineer": {
        "description": "Designs mechanical systems and products.",
        "skills": ["CAD", "SolidWorks", "AutoCAD", "Thermodynamics"],
        "recommended_certs": ["CSWP", "AutoCAD Certified"],
        "domains": ["ME"]
    },
     "Robotics Engineer": {
        "description": "Designs and builds robots.",
        "skills": ["ROS", "C++", "Python", "Control Systems", "Kinematics"],
        "recommended_certs": ["Robotics Software Engineer", "Control Systems"],
        "domains": ["ME", "ECE", "CSE"]
    },

    # CE
    "Structural Engineer": {
        "description": "Designs load-bearing structures.",
        "skills": ["AutoCAD", "STAAD.Pro", "Structural Analysis", "Revit"],
        "recommended_certs": ["Structural Engineering Verification", "Revit Structure"],
        "domains": ["CE"]
    },
    "Construction Manager": {
        "description": "Oversees construction projects.",
        "skills": ["Project Management", "Cost Estimation", "Safety Regulations"],
        "recommended_certs": ["PMP", "CCM"],
        "domains": ["CE"]
    },

    # General / Default
    "General Specialist": {
        "description": "A versatile role requiring broad knowledge.",
        "skills": ["Communication", "Problem Solving", "Project Management"],
        "recommended_certs": ["PMP", "Scrum Master"],
        "domains": []
    }
}

# Branch -> List of Roles mapping
DOMAIN_KEYWORDS = {
    # Computer Science
    "CSE": ["Software Developer", "Web Developer", "Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "App Developer"],
    "Computer Science": ["Software Developer", "Web Developer", "Data Scientist", "Machine Learning Engineer", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "App Developer"],
    "Information Technology": ["Software Developer", "Web Developer", "Data Scientist", "Machine Learning Engineer", "Cloud Engineer"],
    
    # Electronics
    "ECE": ["Embedded Systems Engineer", "VLSI Engineer", "Communication Engineer", "IoT Engineer", "Robotics Engineer", "Network Engineer"],
    "Electronics": ["Embedded Systems Engineer", "VLSI Engineer", "Communication Engineer"],
    
    # Electrical
    "EEE": ["Power Systems Engineer", "Electrical Design Engineer", "Control Systems Engineer", "Renewable Energy Engineer"],
    "Electrical": ["Power Systems Engineer", "Electrical Design Engineer", "Control Systems Engineer"],
    
    # Mechanical
    "Mechanical": ["Mechanical Design Engineer", "Automobile Engineer", "HVAC Engineer", "Aerospace Engineer", "Manufacturing Engineer", "Robotics Engineer"],
    "ME": ["Mechanical Design Engineer", "Automobile Engineer", "HVAC Engineer", "Aerospace Engineer", "Manufacturing Engineer", "Robotics Engineer"],
    
    # Civil
    "Civil": ["Structural Engineer", "Site Engineer", "Construction Manager", "Surveyor", "Geotechnical Engineer"],
    "CE": ["Structural Engineer", "Site Engineer", "Construction Manager", "Surveyor", "Geotechnical Engineer"],
    
    # Biotech
    "Biotech": ["Biomedical Engineer", "Clinical Researcher", "Lab Scientist", "Pharma R&D"],
    "Biomedical": ["Biomedical Engineer", "Clinical Researcher", "Medical Imaging Specialist"],
    
    # Chemical
    "Chemical": ["Process Engineer", "Petroleum Engineer", "Materials Engineer", "Quality Control Engineer"],
    
    # Others
    "Aerospace": ["Aircraft Design Engineer", "Flight Testing Engineer", "Propulsion Engineer"],
    "Automobile": ["Vehicle Design Engineer", "EV Systems Engineer", "Automotive Testing Engineer"],
}
