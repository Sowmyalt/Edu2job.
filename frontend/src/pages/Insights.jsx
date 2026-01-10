import { useState, useEffect } from 'react';
import api from '../api/axios';
import {
    LineChart, Line, AreaChart, Area, BarChart, Bar, RadarChart, Radar, ComposedChart,
    PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { Link } from 'react-router-dom';
import { FaArrowUp, FaArrowRight, FaArrowDown, FaBriefcase } from 'react-icons/fa';

// Premium Color Palette
const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#10b981', '#3b82f6', '#f59e0b'];

const Insights = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInsights = async () => {
            try {
                const response = await api.get('insights/');
                setData(response.data);
            } catch (error) {
                console.error("Error fetching insights", error);
            } finally {
                setLoading(false);
            }
        };
        fetchInsights();
    }, []);

    if (loading) return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
    );

    if (!data || !data.personalized) return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
            <h2 className="text-2xl font-bold text-gray-800">No Insights Available</h2>
            <p className="text-gray-500 mt-2">Please update your profile to see personalized market trends.</p>
            <Link to="/profile" className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                Go to Profile
            </Link>
        </div>
    );

    const { context, market_overview, comparison, career_paths, skill_gap, future_outlook } = data.personalized;

    return (
        <div className="min-h-screen bg-gray-50 p-6 md:p-12 font-sans">
            <div className="max-w-7xl mx-auto space-y-12">

                {/* Header */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
                    <div>
                        <h1 className="text-3xl font-bold" style={{ color: 'var(--primary)' }}>
                            Market Insights for <span className="text-indigo-600">{context.specialization}</span>
                        </h1>
                        <p className="text-gray-500 mt-2">
                            Real-time intelligence based on your profile and {context.degree} background.
                        </p>
                    </div>
                    <Link to="/dashboard" className="mt-4 md:mt-0 text-indigo-600 font-semibold hover:text-indigo-800 transition">
                        &larr; Back to Dashboard
                    </Link>
                </div>

                {/* Section 1: Market Overview (Trend) */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover-effect">
                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h2 className="text-xl font-bold" style={{ color: 'var(--primary)' }}>Market Demand Trend</h2>
                            <p className="text-sm text-gray-500">Job availability over 5 years (Historical & Projected)</p>
                        </div>
                        <span className={`px-4 py-1 rounded-full text-sm font-semibold ${future_outlook.verdict === 'Rising' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'}`}>
                            {future_outlook.verdict} Demand
                        </span>
                    </div>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart data={market_overview}>
                                <defs>
                                    <linearGradient id="professionalGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stopColor="#1f3e72" stopOpacity={0.9} />
                                        <stop offset="100%" stopColor="#1f3e72" stopOpacity={0.4} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                                <XAxis
                                    dataKey="year"
                                    tick={{ fill: '#4b5563', fontSize: 12, fontWeight: 500 }}
                                    axisLine={false}
                                    tickLine={false}
                                    dy={10}
                                />
                                <YAxis
                                    hide={false}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#6b7280', fontSize: 12 }}
                                    width={30}
                                />
                                <Tooltip
                                    cursor={{ fill: 'rgba(31, 62, 114, 0.05)' }}
                                    contentStyle={{ borderRadius: '0px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                />
                                <Bar dataKey="demand" barSize={40} fill="url(#professionalGradient)" radius={[0, 0, 0, 0]} />
                                <Line
                                    type="monotone"
                                    dataKey="demand"
                                    stroke="#ea580c"
                                    strokeWidth={3}
                                    dot={{ r: 5, fill: '#ea580c', strokeWidth: 2, stroke: '#fff' }}
                                    activeDot={{ r: 7 }}
                                />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Grid: Comparison & Skill Gap */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    {/* Section 2: Where You Stand */}
                    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover-effect">
                        <h2 className="text-xl font-bold mb-6" style={{ color: 'var(--primary)' }}>Where You Stand</h2>
                        <p className="text-sm text-gray-500 mb-6">Salary & Demand comparison vs other fields</p>

                        <div className="space-y-6">
                            {comparison.map((item, idx) => (
                                <div key={idx} className="mb-4 last:mb-0">
                                    <div className="flex justify-between items-center mb-2">
                                        <h4 className="font-bold text-gray-800">{item.name}</h4>
                                    </div>

                                    {/* Demand Bar */}
                                    <div className="mb-3">
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-gray-500 font-semibold">Demand Score</span>
                                            <span className="text-[#1f3e72] font-bold">{item.demand}/100</span>
                                        </div>
                                        <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                                            <div
                                                className="h-full rounded-full"
                                                style={{ width: `${item.demand}%`, background: '#1f3e72' }}
                                            />
                                        </div>
                                    </div>

                                    {/* Salary Bar (Normalized Visual) */}
                                    <div>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-gray-500 font-semibold">Avg Salary</span>
                                            <span className="text-orange-600 font-bold">₹{item.salary.toLocaleString('en-IN')}</span>
                                        </div>
                                        <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                                            <div
                                                className="h-full rounded-full bg-orange-500"
                                                style={{ width: `${Math.min((item.salary / 2000000) * 100, 100)}%` }} // Assumes 20 LPA as max visual cap
                                            />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Section 4: Skill Gap */}
                    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover-effect">
                        <h2 className="text-xl font-bold mb-6" style={{ color: 'var(--primary)' }}>Skill Gap Analysis</h2>
                        <p className="text-sm text-gray-500 mb-6">Your skills vs Market Top Demands</p>

                        <div className="h-80">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart outerRadius={90} data={skill_gap}>
                                    <PolarGrid stroke="#e5e7eb" />
                                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#4b5563', fontSize: 12 }} />
                                    <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
                                    <Radar name="Market Need" dataKey="A" stroke="#1f3e72" fill="#1f3e72" fillOpacity={0.25} />
                                    <Radar name="You" dataKey="B" stroke="#8b5cf6" fill="rgb(255, 136, 0)" fillOpacity={0.5} />
                                    <Legend />
                                    <Tooltip />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Section 3: Career Paths */}
                <div>
                    <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--primary)' }}>Recommended Career Paths</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {career_paths.map((path, idx) => (
                            <div key={idx} className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm transition group hover-effect">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="p-3 bg-indigo-50 rounded-lg text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition">
                                        <FaBriefcase size={20} />
                                    </div>
                                    <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full ${path.growth === 'High Growth' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                                        }`}>
                                        {path.growth}
                                    </span>
                                </div>
                                <h3 className="text-lg font-bold text-gray-800">{path.title}</h3>
                                <p className="text-sm text-gray-500 mt-2">
                                    {path.roles || `Aligned with your ${context.specialization} background.`}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Section 5: Future Outlook Summary */}
                {/* Section 5: Future Outlook Summary (Hero Style) */}
                <div className="shadow-xl p-8 md:p-12 relative overflow-hidden" style={{ background: 'var(--black)', color: 'white' }}>

                    {/* Hero Effects */}
                    <div className="white-gradient" style={{ top: '-10%', left: '-10%', opacity: 0.6 }} />


                    <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-10">
                        {/* Text Section */}
                        <div className="flex-1">
                            {/* Title with Orange Circle Accent */}
                            <div className="relative inline-block mb-6">
                                <div className="absolute -top-4 -right-6 w-10 h-10 rounded-full -z-10" style={{ background: 'var(--orange-gradient)' }} />
                                <h2 className="text-4xl md:text-5xl font-semibold flex items-center gap-4">
                                    Future Outlook: <span style={{ color: future_outlook.verdict === 'Rising' ? '#4ade80' : '#facc15' }}>{future_outlook.verdict}</span>
                                </h2>
                            </div>

                            <p className="text-gray-300 text-lg md:text-xl leading-relaxed mb-10 max-w-2xl">
                                {future_outlook.summary}
                            </p>

                            <div>
                                <h4 className="text-sm font-bold uppercase tracking-wider mb-6 text-gray-400">Key Drivers</h4>
                                <div className="flex flex-wrap gap-4">
                                    {future_outlook.impact_factors.map((factor, idx) => (
                                        <span key={idx} className="px-5 py-2 rounded-lg text-sm font-semibold border border-white/10"
                                            style={{ background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(5px)' }}>
                                            {factor}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Image Section (Hero Style) */}
                        <div className="hidden md:block">
                            <div style={{
                                width: '20rem',
                                height: '25rem',
                                overflow: 'hidden',
                                borderRadius: '15rem 15rem 0 0',
                                border: '8px solid rgba(255,255,255,0.12)'
                            }}>
                                <img
                                    src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?q=80&w=1000&auto=format&fit=crop"
                                    alt="Future Career Outlook"
                                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                />
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Insights;
