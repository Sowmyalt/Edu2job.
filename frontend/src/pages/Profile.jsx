import { useState, useEffect } from 'react';
import api from '../api/axios';
import { Link } from 'react-router-dom';
import { DEGREES, SPECIALIZATIONS, CGPA_RANGES, YEARS, STATES, getColleges } from '../data/educationOptions';

const Profile = () => {
    const [profile, setProfile] = useState({});
    const [gpa, setGpa] = useState('');
    const [major, setMajor] = useState('');
    const [education, setEducation] = useState([]);
    const [certificates, setCertificates] = useState([]);
    const [skills, setSkills] = useState([]);
    const [loading, setLoading] = useState(true);

    // New Entry States
    const [newEdu, setNewEdu] = useState({ degree: '', specialization: '', institution: '', cgpa: '', year: '' });
    const [selectedState, setSelectedState] = useState('');
    const [newCert, setNewCert] = useState({ name: '', issuer: '', year: '' });
    const [newSkill, setNewSkill] = useState('');
    const [eduError, setEduError] = useState('');

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('profile/');
                setProfile(response.data);

                const info = response.data.academic_info || {};
                setGpa(info.gpa || '');
                setMajor(info.major || '');
                setEducation(info.education || []);
                setCertificates(info.certificates || []);
                setSkills(info.skills || []);
            } catch (error) {
                console.error("Error fetching profile", error);
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const handleSave = async () => {
        const academic_info = {
            gpa,
            major,
            major,
            education,
            certificates,
            skills
        };
        try {
            const response = await api.put('profile/', { academic_info });
            console.log("Save Response:", response.data);
            setProfile(response.data); // Update local state with server response
            alert("Profile updated successfully!");
        } catch (error) {
            console.error("Save error", error);
            alert("Failed to update profile.");
        }
    };

    const addEducation = () => {
        setEduError('');
        // Validation
        if (!newEdu.degree || !newEdu.institution || !newEdu.year) {
            setEduError("Please fill in Degree, Institution and Year.");
            return;
        }
        if (!newEdu.cgpa) {
            setEduError("Please select a CGPA range.");
            return;
        }

        let finalInstitution = newEdu.institution;
        if (newEdu.institution === "Other / Not Listed") {
            if (!newEdu.customInstitution) {
                setEduError("Please enter your Institution Name.");
                return;
            }
            finalInstitution = newEdu.customInstitution;
        }

        const entry = { ...newEdu, institution: finalInstitution };
        delete entry.customInstitution; // Clean up

        setEducation([...education, entry]);
        setNewEdu({ degree: '', specialization: '', institution: '', cgpa: '', year: '' });
        setSelectedState('');
    };

    const removeEducation = (index) => {
        const updated = education.filter((_, i) => i !== index);
        setEducation(updated);
    };

    const addCertificate = () => {
        if (newCert.name && newCert.issuer) {
            setCertificates([...certificates, newCert]);
            setNewCert({ name: '', issuer: '', year: '' });
        }
    };

    const removeCertificate = (index) => {
        const updated = certificates.filter((_, i) => i !== index);
        setCertificates(updated);
    };

    const addSkill = () => {
        if (newSkill.trim()) {
            setSkills([...skills, newSkill.trim()]);
            setNewSkill('');
        }
    };

    const removeSkill = (index) => {
        const updated = skills.filter((_, i) => i !== index);
        setSkills(updated);
    };

    if (loading) return <div className="p-8 text-center">Loading...</div>;

    return (
        <div className="min-h-screen relative font-sans p-8 bg-gray-50">

            <div className="max-w-4xl mx-auto bg-white rounded-sm shadow-lg overflow-hidden border border-gray-100 relative z-10">
                <div className="p-8 border-b border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-3xl font-bold" style={{ color: 'var(--primary)' }}>Edit Profile</h1>
                        <Link to="/dashboard" className="text-gray-500 hover:text-[#1f3e72] font-semibold flex items-center transition">
                            &larr; Back to Dashboard
                        </Link>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-600 mb-1">Username</label>
                            <input type="text" value={profile.username || ''} disabled
                                className="w-full p-3 bg-gray-100 border border-gray-200 rounded-sm text-gray-700 font-medium" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-600 mb-1">Email</label>
                            <input type="text" value={profile.email || ''} disabled
                                className="w-full p-3 bg-gray-100 border border-gray-200 rounded-sm text-gray-700 font-medium" />
                        </div>
                    </div>
                </div>

                <div className="p-8 bg-white border-b border-gray-100">
                    <h2 className="text-xl font-bold mb-4 border-l-4 border-[#1f3e72] pl-3" style={{ color: 'var(--primary)' }}>Academic Overview</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-600 mb-1">Major / Field of Study</label>
                            <input
                                type="text"
                                value={major}
                                onChange={(e) => setMajor(e.target.value)}
                                placeholder="e.g. Computer Science"
                                className="w-full p-3 bg-white border border-gray-200 rounded-sm text-gray-700 placeholder-gray-400 focus:ring-2 focus:ring-blue-500 outline-none transition"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-600 mb-1">CGPA (Scale of 10)</label>
                            <input
                                type="number"
                                step="0.1"
                                min="0"
                                max="10.0"
                                value={gpa}
                                onChange={(e) => setGpa(e.target.value)}
                                placeholder="e.g. 8.5"
                                className="w-full p-3 bg-white border border-gray-200 rounded-sm text-gray-700 placeholder-gray-400 focus:ring-2 focus:ring-[#1f3e72]/20 focus:border-[#1f3e72] outline-none transition"
                            />
                        </div>
                    </div>
                </div>

                <div className="p-8 bg-gray-50/50">
                    {/* Education Section */}
                    <div className="mb-10">
                        <h2 className="text-xl font-bold mb-4 border-l-4 border-[#1f3e72] pl-3" style={{ color: 'var(--primary)' }}>Education</h2>

                        {education.map((edu, index) => (
                            <div key={index} className="flex justify-between items-center bg-white p-4 rounded-sm shadow-sm mb-3 border border-gray-200">
                                <div>
                                    <h4 className="font-bold text-gray-800">{edu.degree} <span className="text-gray-500 font-normal">{edu.specialization ? `in ${edu.specialization}` : ''}</span></h4>
                                    <p className="text-gray-600 text-sm">{edu.institution} • {edu.year} {edu.cgpa ? `• CGPA: ${edu.cgpa}` : ''}</p>
                                </div>
                                <button onClick={() => removeEducation(index)} className="text-gray-400 hover:text-gray-600 text-sm font-semibold">Remove</button>
                            </div>
                        ))}

                        <div className="bg-white p-5 rounded-sm border border-gray-200 mt-4 shadow-sm">
                            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Add New Education</h3>
                            <div className="grid grid-cols-1 gap-3 mb-3">
                                {/* Degree & Specialization */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={newEdu.degree} onChange={e => setNewEdu({ ...newEdu, degree: e.target.value })}>
                                        <option value="">Select Degree</option>
                                        {DEGREES.map(d => <option key={d} value={d}>{d}</option>)}
                                    </select>

                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={newEdu.specialization} onChange={e => setNewEdu({ ...newEdu, specialization: e.target.value })}>
                                        <option value="">Select Specialization</option>
                                        {Object.entries(SPECIALIZATIONS).map(([group, specs]) => (
                                            <optgroup label={group} key={group}>
                                                {specs.map(s => <option key={s} value={s}>{s}</option>)}
                                            </optgroup>
                                        ))}
                                    </select>
                                </div>

                                {/* State & College */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={selectedState} onChange={e => setSelectedState(e.target.value)}>
                                        <option value="">Select State (for College)</option>
                                        {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                                    </select>

                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={newEdu.institution} onChange={e => setNewEdu({ ...newEdu, institution: e.target.value })} disabled={!selectedState}>
                                        <option value="">Select Institution</option>
                                        {selectedState && getColleges(selectedState).map(c => <option key={c} value={c}>{c}</option>)}
                                    </select>
                                </div>

                                {/* CGPA & Year */}
                                <div className="grid grid-cols-2 gap-2">
                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={newEdu.cgpa} onChange={e => setNewEdu({ ...newEdu, cgpa: e.target.value })}>
                                        <option value="">Select CGPA Range</option>
                                        {CGPA_RANGES.map(r => <option key={r} value={r}>{r}</option>)}
                                    </select>

                                    <select className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700" value={newEdu.year} onChange={e => setNewEdu({ ...newEdu, year: e.target.value })}>
                                        <option value="">Year of Grad</option>
                                        {YEARS.map(y => <option key={y} value={y}>{y}</option>)}
                                    </select>
                                </div>
                            </div>
                            <button onClick={addEducation} className="bg-gray-100 hover:bg-gray-200 text-[#1f3e72] px-4 py-2 rounded-sm text-sm font-bold transition shadow-sm border border-gray-200">
                                + Add Education
                            </button>
                        </div>
                    </div>

                    {/* Certificates Section */}
                    <div className="mb-8">
                        <h2 className="text-xl font-bold mb-4 border-l-4 border-orange-400 pl-3" style={{ color: 'var(--primary)' }}>Certificates</h2>

                        {certificates.map((cert, index) => (
                            <div key={index} className="flex justify-between items-center bg-white p-4 rounded-sm shadow-sm mb-3 border border-gray-200">
                                <div>
                                    <h4 className="font-bold text-gray-800">{cert.name}</h4>
                                    <p className="text-gray-600 text-sm">{cert.issuer} • {cert.year}</p>
                                </div>
                                <button onClick={() => removeCertificate(index)} className="text-red-500 hover:text-red-700 text-sm font-semibold">Remove</button>
                            </div>
                        ))}

                        <div className="bg-white p-5 rounded-sm border border-gray-200 mt-4 shadow-sm">
                            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Add New Certificate</h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                                <input placeholder="Certificate Name" value={newCert.name} onChange={e => setNewCert({ ...newCert, name: e.target.value })} className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700 placeholder-gray-400" />
                                <input placeholder="Issuer" value={newCert.issuer} onChange={e => setNewCert({ ...newCert, issuer: e.target.value })} className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700 placeholder-gray-400" />
                                <input placeholder="Year" value={newCert.year} onChange={e => setNewCert({ ...newCert, year: e.target.value })} className="p-2 border border-gray-200 rounded-sm bg-white text-gray-700 placeholder-gray-400" />
                            </div>
                            <button onClick={addCertificate} className="bg-gray-100 hover:bg-gray-200 text-orange-600 px-4 py-2 rounded-sm text-sm font-bold transition shadow-sm border border-gray-200">
                                + Add Certificate
                            </button>
                        </div>
                    </div>
                    {/* Skills Section */}
                    <div className="mb-8">
                        <h2 className="text-xl font-bold mb-4 border-l-4 border-teal-500 pl-3" style={{ color: 'var(--primary)' }}>Skills</h2>
                        <div className="bg-white p-5 rounded-sm border border-gray-200 shadow-sm">
                            <div className="flex flex-wrap gap-2 mb-4">
                                {skills.map((skill, index) => (
                                    <span key={index} className="px-3 py-1 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold border border-teal-100 flex items-center gap-2">
                                        {skill}
                                        <button onClick={() => removeSkill(index)} className="hover:text-red-500 font-bold">×</button>
                                    </span>
                                ))}
                                {skills.length === 0 && <p className="text-gray-400 text-sm italic">No skills added yet.</p>}
                            </div>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={newSkill}
                                    onChange={(e) => setNewSkill(e.target.value)}
                                    onKeyPress={(e) => e.key === 'Enter' && addSkill()}
                                    placeholder="Add a skill (e.g. Python, Leadership)"
                                    className="flex-1 p-2 border border-gray-200 rounded-sm bg-white text-gray-700 placeholder-gray-400 focus:ring-2 focus:ring-teal-500 outline-none transition"
                                />
                                <button onClick={addSkill} className="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-sm text-sm font-bold transition shadow-sm">
                                    Add
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="p-6 bg-gray-50 border-t border-gray-200 flex justify-end">
                    <button onClick={handleSave} className="text-white px-8 py-3 rounded-sm font-bold shadow-md"
                        style={{ background: 'var(--blue-gradient)' }}>
                        Save Profile Changes
                    </button>
                </div>
            </div>
        </div >
    );
};

export default Profile;
