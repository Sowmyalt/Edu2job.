export const DEGREES = [
    "B.Tech", "B.E", "B.Sc", "B.Sc (Hons)", "BCA", "B.Arch", "B.Des",
    "B.Com", "BBA", "BA", "M.Tech", "M.E", "M.Sc", "MCA", "MBA",
    "PhD", "Diploma", "Integrated M.Tech", "Integrated MSc", "Other"
];

export const SPECIALIZATIONS = {
    "Engineering / Tech": [
        "Computer Science and Engineering (CSE)",
        "CSE (AI & ML)",
        "CSE (Data Science)",
        "CSE (Cyber Security)",
        "Information Technology (IT)",
        "Electronics and Communication Engineering (ECE)",
        "Electrical and Electronics Engineering (EEE)",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Biotechnology",
        "Robotics",
        "Mechatronics"
    ],
    "Science / Others": [
        "Artificial Intelligence",
        "Data Science",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Statistics",
        "Economics",
        "Commerce",
        "Management",
        "Design",
        "Architecture",
        "Other"
    ]
};

export const CGPA_RANGES = [
    "10.0",
    "9.0 – 10.0",
    "8.0 – 8.9",
    "7.0 – 7.9",
    "6.0 – 6.9",
    "Below 6.0"
];

export const YEARS = [
    "2018", "2019", "2020", "2021", "2022", "2023",
    "2024", "2025", "2026", "2027", "2028", "2029"
];

export const STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
];

// Sample Colleges - In a real app this would be a massive list or API
export const COLLEGES_BY_STATE = {
    "Karnataka": [
        "Indian Institute of Science (IISc), Bangalore",
        "IIIT Bangalore",
        "RV College of Engineering, Bangalore",
        "PES University, Bangalore",
        "MS Ramaiah Institute of Technology, Bangalore",
        "BMS College of Engineering, Bangalore",
        "Manipal Institute of Technology, Manipal",
        "National Institute of Technology (NITK), Surathkal"
    ],
    "Maharashtra": [
        "IIT Bombay",
        "Institute of Chemical Technology (ICT), Mumbai",
        "VJTI Mumbai",
        "College of Engineering Pune (COEP)",
        "Symbiosis Institute of Technology, Pune",
        "VNIT Nagpur"
    ],
    "Delhi": [
        "IIT Delhi",
        "Delhi Technological University (DTU)",
        "IIIT Delhi",
        "Netaji Subhas University of Technology (NSUT)",
        "Jawaharlal Nehru University (JNU)",
        "Jamia Millia Islamia"
    ],
    "Tamil Nadu": [
        "IIT Madras",
        "Anna University, Chennai",
        "NIT Trichy",
        "Vellore Institute of Technology (VIT)",
        "SRM Institute of Science and Technology",
        "Amrita Vishwa Vidyapeetham"
    ],
    "Uttar Pradesh": [
        "IIT Kanpur",
        "IIT BHU (Varanasi)",
        "Amity University, Noida",
        "Shiv Nadar University",
        "MNNIT Allahabad"
    ],
    "Telangana": [
        "IIT Hyderabad",
        "IIIT Hyderabad",
        "NIT Warangal",
        "BITS Pilani, Hyderabad Campus",
        "Osmania University"
    ]
    // Add default behavior for other states
};

export const getColleges = (state) => {
    const list = COLLEGES_BY_STATE[state] || [];
    return [...list, "Other / Not Listed"];
};
