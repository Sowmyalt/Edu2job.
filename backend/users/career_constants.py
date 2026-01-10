CAREER_PATHS_DB = {
    # COMPUTER & IT
    "cse": {
        "paths": [
            {"title": "Software Engineering Path", "roles": "Backend / Full-Stack / Systems Engineer", "growth": "High Growth"},
            {"title": "Data & AI Path", "roles": "Data Analyst → Data Scientist → ML Engineer", "growth": "High Growth"},
            {"title": "Cloud & DevOps Path", "roles": "Cloud Engineer → DevOps → SRE", "growth": "Rising"},
            {"title": "Cybersecurity Path", "roles": "Security Analyst → Security Engineer", "growth": "Stable"},
            {"title": "Product Leadership", "roles": "Senior Engineer → Tech Lead → PM", "growth": "Lucrative"}
        ],
        "insight": "Most flexible branch, easiest to switch domains."
    },
    "it": "cse",
    "software": "cse",

    "ai": {
        "paths": [
            {"title": "Applied AI Engineer Path", "roles": "ML Engineer → AI Engineer", "growth": "High Growth"},
            {"title": "Data Analytics Path", "roles": "Analyst → Senior Analyst → Decision Scientist", "growth": "Stable"},
            {"title": "Research Path", "roles": "AI Researcher → PhD / R&D roles", "growth": "Niche"},
            {"title": "AI Product Path", "roles": "AI Consultant → AI Product Manager", "growth": "Rising"}
        ],
        "insight": "High demand but requires continuous upskilling."
    },
    "ml": "ai",
    "data science": "ai",

    "cyber": {
        "paths": [
            {"title": "Security Operations Path", "roles": "SOC Analyst → Threat Hunter", "growth": "High Growth"},
            {"title": "Offensive Security Path", "roles": "Ethical Hacker → Red Team Engineer", "growth": "Niche"},
            {"title": "Security Engineering", "roles": "Security Engineer → Cloud Security Architect", "growth": "Rising"},
            {"title": "Governance & Risk Path", "roles": "GRC Analyst → Compliance Lead", "growth": "Stable"}
        ],
        "insight": "Stable, recession-resistant career."
    },

    # ELECTRONICS
    "ece": {
        "paths": [
            {"title": "Embedded Systems Path", "roles": "Embedded Engineer → Firmware Architect", "growth": "High Growth"},
            {"title": "VLSI / Semiconductor", "roles": "Design Engineer → Physical Design / Verification", "growth": "Lucrative"},
            {"title": "Telecom & Networking", "roles": "Network Engineer → 5G/6G Specialist", "growth": "Stable"},
            {"title": "Software Transition", "roles": "Software Engineer / Data Engineer", "growth": "Flexible"}
        ],
        "insight": "Hardware + software combo = strong career."
    },
    "communication": "ece",

    "eee": {
        "paths": [
            {"title": "Power Systems Path", "roles": "Electrical Engineer → Grid / Power Analyst", "growth": "Stable"},
            {"title": "Renewable Energy Path", "roles": "Solar / Wind Engineer → Energy Consultant", "growth": "Rising"},
            {"title": "Automation & Control", "roles": "Control Engineer → Industrial Automation Lead", "growth": "High Growth"},
            {"title": "IT / Analytics Path", "roles": "IT / Analytics roles", "growth": "Flexible"}
        ],
        "insight": "Energy transition boosts demand."
    },
    "electrical": "eee",

    "eie": {
        "paths": [
            {"title": "Instrumentation & Control", "roles": "Instrumentation Engineer → Control Specialist", "growth": "Stable"},
            {"title": "Industrial Automation", "roles": "PLC/SCADA Engineer", "growth": "Rising"},
            {"title": "Process Industry Path", "roles": "Process Control Engineer", "growth": "Stable"}
        ],
        "insight": "Strong in manufacturing & process industries."
    },
    "instrumentation": "eie",

    # CORE ENGINEERING
    "mechanical": {
        "paths": [
            {"title": "Design & Manufacturing", "roles": "Design Engineer → Product Engineer", "growth": "Stable"},
            {"title": "Automotive & EV Path", "roles": "Vehicle Engineer → EV Systems Engineer", "growth": "High Growth"},
            {"title": "Industrial Operations", "roles": "Production → Plant Manager", "growth": "Stable"},
            {"title": "Mech + Software Path", "roles": "Simulation / Robotics / Automation", "growth": "Rising"}
        ],
        "insight": "EV + automation is the growth lever."
    },
    "mech": "mechanical",

    "civil": {
        "paths": [
            {"title": "Construction Mgmt", "roles": "Site Engineer → Project Manager", "growth": "Stable"},
            {"title": "Structural Engineering", "roles": "Structural Analyst → Design Consultant", "growth": "Stable"},
            {"title": "Infrastructure Path", "roles": "PSU / Smart Cities roles", "growth": "Stable"},
            {"title": "Sustainability Path", "roles": "Environmental / Transport Planner", "growth": "Rising"}
        ],
        "insight": "Stable, long-term growth career."
    },

    "chemical": {
        "paths": [
            {"title": "Process Engineering", "roles": "Process Engineer → Plant Operations Lead", "growth": "Stable"},
            {"title": "Energy & Materials", "roles": "Battery / Petrochemical Engineer", "growth": "Rising"},
            {"title": "Pharma & Biotech Path", "roles": "Process Development Engineer", "growth": "Stable"},
            {"title": "Safety & Compliance", "roles": "Safety Engineer → HSE Manager", "growth": "Stable"}
        ],
        "insight": "Strong for higher studies & core industry."
    },

    "metallurg": {
        "paths": [
            {"title": "Materials Engineering", "roles": "Materials Scientist → R&D Engineer", "growth": "Niche"},
            {"title": "Manufacturing Quality", "roles": "QA Engineer → Process Improvement Lead", "growth": "Stable"},
            {"title": "Defense & Industry", "roles": "PSU / Research Labs", "growth": "Stable"}
        ],
        "insight": "Niche but valuable in core sectors."
    },

    # SPECIALIZED
    "aerospace": {
        "paths": [
            {"title": "Aircraft Design Path", "roles": "Design Engineer → Aerospace Scientist", "growth": "Niche"},
            {"title": "Defense & Research", "roles": "DRDO / ISRO / PSU", "growth": "Stable"},
            {"title": "Maint & Operations", "roles": "Aircraft Systems Engineer", "growth": "Stable"}
        ],
        "insight": "Highly competitive, research-heavy."
    },
    
    "biotechnology": {
        "paths": [
            {"title": "R&D Path", "roles": "Research Scientist → PhD", "growth": "Niche"},
            {"title": "Bioprocess Industry", "roles": "Bioprocess Engineer", "growth": "Stable"},
            {"title": "Health Data Path", "roles": "Bioinformatics Analyst", "growth": "Rising"}
        ],
        "insight": "Research-oriented, niche growth."
    },
    "biotech": "biotechnology",

    "biomedical": {
        "paths": [
            {"title": "Medical Devices Path", "roles": "Device Engineer → Product Specialist", "growth": "High Growth"},
            {"title": "Healthcare Tech", "roles": "Clinical Engineer", "growth": "Stable"},
            {"title": "Health Analytics", "roles": "Medical Data Analyst", "growth": "Rising"}
        ],
        "insight": "Healthcare tech is expanding."
    },

    "robotics": {
        "paths": [
            {"title": "Robotics Engineering", "roles": "Robotics Engineer → Automation Architect", "growth": "High Growth"},
            {"title": "Industrial Automation", "roles": "Controls & PLC Engineer", "growth": "Stable"},
            {"title": "Robotics + AI Path", "roles": "Intelligent Systems Engineer", "growth": "High Growth"}
        ],
        "insight": "Interdisciplinary & future-ready."
    },
    "mechatronics": "robotics",

    "iot": {
        "paths": [
            {"title": "IoT Systems Path", "roles": "IoT Engineer → Solutions Architect", "growth": "High Growth"},
            {"title": "Embedded & Edge", "roles": "Embedded Systems Engineer", "growth": "Rising"},
            {"title": "Smart Infrastructure", "roles": "Industrial IoT Engineer", "growth": "Rising"}
        ],
        "insight": "IoT works best combined with another core skill."
    },

    "cloud": {
        "paths": [
            {"title": "Cloud Engineering", "roles": "Cloud Engineer → Cloud Architect", "growth": "High Growth"},
            {"title": "DevOps Path", "roles": "DevOps Engineer → SRE", "growth": "High Growth"},
            {"title": "Cloud Security", "roles": "Cloud Security Engineer", "growth": "Rising"}
        ],
        "insight": "High demand across industries."
    }
}
