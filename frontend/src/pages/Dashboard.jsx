import { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import AuthContext from '../context/AuthContext';
import { Link } from 'react-router-dom';
import Header from '../components/header/header';

const Dashboard = () => {
    const [history, setHistory] = useState([]);

    const { user } = useContext(AuthContext);

    // Feedback State
    const [isFeedbackModalOpen, setIsFeedbackModalOpen] = useState(false);
    const [currentPredictionId, setCurrentPredictionId] = useState(null);
    const [feedbackRating, setFeedbackRating] = useState(0);
    const [feedbackText, setFeedbackText] = useState("");
    const [submittingFeedback, setSubmittingFeedback] = useState(false);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get('dashboard/');
                setHistory(response.data);
            } catch (error) {
                console.error("Error fetching history", error);
            }
        };
        fetchHistory();
    }, []);

    const handlePredict = async () => {
        try {
            const response = await api.post('predict/');
            // Refresh history
            const historyResponse = await api.get('dashboard/');
            setHistory(historyResponse.data);

            // Open feedback for the new prediction immediately
            if (response.data.history_id) {
                openFeedbackModal(response.data.history_id);
            }

            alert(`Prediction: ${response.data.prediction}`);
        } catch (error) {
            console.error("Prediction failed", error);
            alert("Prediction failed. Make sure your profile has GPA and Major.");
        }
    };

    const openFeedbackModal = (id) => {
        setCurrentPredictionId(id);
        setFeedbackRating(0);
        setFeedbackText("");
        setIsFeedbackModalOpen(true);
    };

    const submitFeedback = async () => {
        if (!currentPredictionId) return;
        setSubmittingFeedback(true);
        try {
            await api.patch(`predictions/${currentPredictionId}/feedback/`, {
                rating: feedbackRating,
                feedback_text: feedbackText
            });
            // Refresh history to show updated feedback status (if we display it)
            const historyResponse = await api.get('dashboard/');
            setHistory(historyResponse.data);

            setIsFeedbackModalOpen(false);
            alert("Thank you for your feedback!");
        } catch (error) {
            console.error("Feedback submission failed", error);
            alert("Failed to submit feedback.");
        } finally {
            setSubmittingFeedback(false);
        }
    };

    return (
        <div className="min-h-screen relative font-sans bg-gray-50">
            {/* Navbar */}
            <Header />

            {/* Content */}
            <div className="max-w-6xl mx-auto p-8 relative z-10">
                <header className="mb-10 text-center">
                    <h1 className="text-4xl font-extrabold mb-2" style={{ color: 'var(--primary)' }}>Dashboard</h1>
                    <p className="text-gray-500 text-lg">Track your career predictions and progress</p>
                    <div className="flex justify-center space-x-4 mt-6">
                        <button
                            onClick={handlePredict}
                            className="text-white px-8 py-3 rounded-sm font-bold shadow-lg hover-effect"
                            style={{ background: 'var(--blue-gradient)' }}
                        >
                            Predict Career Now
                        </button>
                        <Link
                            to="/insights"
                            className="bg-white text-[#1f3e72] border border-gray-200 px-8 py-3 rounded-sm font-bold shadow-sm hover-effect flex items-center"
                        >
                            View Market Trends &rarr;
                        </Link>
                    </div>
                </header>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    <div className="bg-white p-6 rounded-sm shadow-md border border-gray-100 hover-effect">
                        <h3 className="text-gray-500 text-sm font-semibold uppercase">Total Predictions</h3>
                        <p className="text-3xl font-bold mt-2" style={{ color: 'var(--primary)' }}>{history.length}</p>
                    </div>
                    <div className="bg-white p-6 rounded-sm shadow-md border border-gray-100 hover-effect">
                        <h3 className="text-gray-500 text-sm font-semibold uppercase">Latest Activity</h3>
                        <p className="text-xl font-bold text-gray-800 mt-2">
                            {history.length > 0 ? new Date(history[0].timestamp).toLocaleDateString() : 'N/A'}
                        </p>
                    </div>
                    <div className="bg-white p-6 rounded-sm shadow-md border border-gray-100 hover-effect">
                        <h3 className="text-gray-500 text-sm font-semibold uppercase">Profile Status</h3>
                        {/* Placeholder logic for profile completion */}
                        <p className="text-xl font-bold mt-2" style={{ color: 'var(--primary)' }}>Active</p>
                    </div>
                </div>

                <div className="bg-white shadow-lg rounded-sm overflow-hidden border border-gray-100">
                    <div className="px-8 py-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                        <h2 className="text-xl font-bold" style={{ color: 'var(--primary)' }}>Prediction History</h2>
                    </div>

                    <div className="overflow-x-auto max-h-[75vh] overflow-y-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 sticky top-0 z-10 shadow-sm">
                                <tr>
                                    <th className="px-8 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
                                    <th className="px-8 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Result</th>
                                    <th className="px-8 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Details</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {history.map((item) => (
                                    <tr key={item.id} className="hover:bg-gray-50 transition border-b border-gray-100 last:border-0">
                                        <td className="px-6 py-4">
                                            <div className="text-sm text-gray-900 font-medium">
                                                {new Date(item.timestamp).toLocaleDateString()}
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {new Date(item.timestamp).toLocaleTimeString()}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-sm text-xs font-bold bg-gray-100 text-[#1f3e72] border border-gray-200">
                                                {item.prediction_data.result}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-500">
                                            {item.prediction_data.details ? (
                                                <div className="space-y-4">
                                                    {item.prediction_data.details.slice(0, 3).map((pred, idx) => (
                                                        <div key={idx} className="bg-gray-50 p-3 rounded-sm border border-gray-200 hover-effect">
                                                            <div className="flex justify-between items-center mb-1">
                                                                <h4 className="font-bold text-gray-800">{pred.role}</h4>
                                                                <span className="text-xs font-bold bg-orange-50 text-orange-600 px-2 py-0.5 rounded border border-orange-100">
                                                                    {pred.match_score}% Match
                                                                </span>
                                                            </div>
                                                            <p className="text-xs text-gray-600 mb-2 italic">"{pred.justification}"</p>

                                                            {/* Recommended/Missing Skills */}
                                                            {pred.missing_skills && pred.missing_skills.length > 0 && (
                                                                <div className="mb-2">
                                                                    <span className="text-xs font-semibold text-gray-500 block mb-1">Recommended Skills:</span>
                                                                    <div className="flex flex-wrap gap-1">
                                                                        {pred.missing_skills.slice(0, 3).map(skill => (
                                                                            <span key={skill} className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-[10px] rounded border border-gray-200">
                                                                                {skill}
                                                                            </span>
                                                                        ))}
                                                                    </div>
                                                                </div>
                                                            )}
                                                            {pred.recommended_certs && pred.recommended_certs.length > 0 && (
                                                                <div>
                                                                    <span className="text-xs font-semibold text-gray-500 block mb-1">Key Certifications:</span>
                                                                    <div className="flex flex-wrap gap-1">
                                                                        {pred.recommended_certs.slice(0, 2).map(cert => (
                                                                            <span key={cert} className="px-1.5 py-0.5 bg-gray-100 text-[#1f3e72] text-[10px] rounded border border-gray-200">
                                                                                {cert}
                                                                            </span>
                                                                        ))}
                                                                    </div>
                                                                </div>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : (
                                                <div className="text-xs text-gray-400 italic">
                                                    Basic prediction data only.
                                                </div>
                                            )}

                                            <div className="mt-4 pt-2 border-t border-gray-100 flex items-center justify-between">
                                                {item.rating ? (
                                                    <div className="text-xs text-gray-500 flex items-center">
                                                        <span className="mr-1">✓ Feedback sent</span>
                                                        <span className="flex text-orange-400">
                                                            {[...Array(item.rating)].map((_, i) => (
                                                                <span key={i}>★</span>
                                                            ))}
                                                        </span>
                                                    </div>
                                                ) : (
                                                    <button
                                                        onClick={() => openFeedbackModal(item.id)}
                                                        className="text-xs text-[#1f3e72] hover:underline font-medium"
                                                    >
                                                        Give Feedback
                                                    </button>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                {history.length === 0 && (
                                    <tr>
                                        <td colSpan="3" className="px-8 py-10 text-center text-gray-500">
                                            <p className="mb-2">No predictions yet.</p>
                                            <button onClick={handlePredict} className="text-sm bg-gray-100 text-[#1f3e72] px-3 py-1 rounded-sm hover:bg-gray-200 transition">Make your first prediction!</button>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>


            {/* Feedback Modal */}
            {
                isFeedbackModalOpen && (
                    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
                        <div className="bg-white rounded-sm shadow-2xl max-w-md w-full p-6 animate-fade-in-up">
                            <div className="text-center mb-6">
                                <h3 className="text-xl font-bold" style={{ color: 'var(--primary)' }}>Rate this Prediction</h3>
                                <p className="text-gray-500 text-sm mt-1">How helpful was this career prediction?</p>
                            </div>

                            <div className="flex justify-center space-x-2 mb-6">
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        onClick={() => setFeedbackRating(star)}
                                        className={`text-3xl transition transform hover:scale-110 focus:outline-none ${star <= feedbackRating ? 'text-orange-400' : 'text-gray-300'
                                            }`}
                                    >
                                        ★
                                    </button>
                                ))}
                            </div>

                            <div className="mb-6">
                                <label className="block text-sm font-medium text-gray-700 mb-2">Additional Comments (Optional)</label>
                                <textarea
                                    value={feedbackText}
                                    onChange={(e) => setFeedbackText(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none h-24 text-gray-700"
                                    placeholder="Tell us more..."
                                ></textarea>
                            </div>

                            <div className="flex space-x-3">
                                <button
                                    onClick={() => setIsFeedbackModalOpen(false)}
                                    className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 font-bold rounded-sm hover:bg-gray-200 transition"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={submitFeedback}
                                    disabled={submittingFeedback || feedbackRating === 0}
                                    className={`flex-1 px-4 py-2 text-white font-bold rounded-sm transition shadow-md ${submittingFeedback || feedbackRating === 0
                                        ? 'bg-gray-400 cursor-not-allowed opacity-50'
                                        : 'hover:shadow-lg'
                                        }`}
                                    style={!(submittingFeedback || feedbackRating === 0) ? { background: 'var(--blue-gradient)' } : {}}
                                >
                                    {submittingFeedback ? 'Sending...' : 'Submit Feedback'}
                                </button>
                            </div>
                        </div>
                    </div>
                )
            }
        </div >
    );
};

export default Dashboard;
