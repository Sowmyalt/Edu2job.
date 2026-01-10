import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import AuthContext from '../context/AuthContext';
import { Link } from 'react-router-dom';
import Header from '../components/header/header';
import './AdminDashboard.css'; // We'll create this or use inline styles for now

const AdminDashboard = () => {
    const { user, logoutUser } = useContext(AuthContext);
    const [stats, setStats] = useState({ total_users: 0, total_predictions: 0, flagged_predictions: 0 });
    const [predictions, setPredictions] = useState([]);
    const [file, setFile] = useState(null);
    const [retrainMsg, setRetrainMsg] = useState("");
    const [loading, setLoading] = useState(true);

    const [activeTab, setActiveTab] = useState('overview');

    const [users, setUsers] = useState([]);
    const [includeFeedback, setIncludeFeedback] = useState(false);

    useEffect(() => {
        fetchStats();
        fetchPredictions();
        fetchUsers();
    }, []);

    const fetchStats = async () => {
        try {
            const res = await api.get('admin/stats/');
            setStats(res.data);
        } catch (err) {
            console.error("Error fetching admin stats", err);
        }
    };

    const fetchPredictions = async () => {
        try {
            const res = await api.get('admin/predictions/');
            setPredictions(res.data);
            setLoading(false);
        } catch (err) {
            console.error("Error fetching predictions", err);
            setLoading(false);
        }
    };

    const fetchUsers = async () => {
        try {
            const res = await api.get('admin/users/');
            setUsers(res.data);
        } catch (err) {
            console.error("Error fetching users", err);
        }
    };

    const handleDeleteUser = async (id) => {
        if (!window.confirm("Are you sure you want to delete this user? This action cannot be undone.")) return;
        try {
            await api.delete(`admin/users/${id}/`);
            fetchUsers();
            fetchStats(); // Update stats as user count changes
        } catch (err) {
            alert("Failed to delete user.");
        }
    };

    const handleFlag = async (id, isFlagged, currentCorrection) => {
        const correction = prompt("Enter correction/feedback details (optional):", currentCorrection || "");
        if (correction === null) return; // Cancelled

        try {
            await api.patch(`admin/predictions/${id}/`, {
                is_flagged: !isFlagged,
                correction: correction
            });
            fetchStats();
            fetchPredictions();
        } catch (err) {
            alert("Failed to update prediction.");
        }
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleRetrain = async () => {
        // Validation: Must have file OR use feedback with existing dataset (backend handles this logic now)
        // But for UX, let's warn if neither.
        if (!file && !includeFeedback) {
            const proceed = window.confirm("No file selected and 'Include Feedback' is unchecked. This will just retrain on the existing dataset. Continue?");
            if (!proceed) return;
        }

        const formData = new FormData();
        if (file) formData.append('file', file);
        formData.append('include_feedback', includeFeedback);

        setRetrainMsg("Processing... please wait.");

        try {
            const res = await api.post('admin/retrain/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setRetrainMsg(res.data.message);
        } catch (err) {
            setRetrainMsg("Error: " + (err.response?.data?.error || err.message));
        }
    };

    if (!user?.is_staff) {
        return (
            <div className="admin-dashboard">
                <Header />
                <div className="dashboard-container" style={{ textAlign: 'center' }}>
                    <h2>Access Denied</h2>
                    <p>You do not have permission to view this page.</p>
                </div>
            </div>
        );
    }

    // Filter predictions based on tabs
    const flaggedPredictions = predictions.filter(p => p.is_flagged);
    const userReviews = predictions.filter(p => p.rating || p.feedback_text);
    const adminCorrections = predictions.filter(p => p.correction);

    const renderTable = (data, showUserFeedback = false, showAdminFeedback = false) => (
        <div className="data-table-container">
            {data.length === 0 ? (
                <p style={{ padding: '20px', color: '#6b7280' }}>No records found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>User</th>
                            <th>Prediction</th>
                            {showUserFeedback && <th>User Rating/Feedback</th>}
                            {showAdminFeedback && <th>Admin Correction</th>}
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map(pred => {
                            let topRole = "Unknown";
                            if (pred.prediction_data) {
                                if (pred.prediction_data.result) topRole = pred.prediction_data.result;
                                else if (pred.prediction_data.top_prediction) topRole = pred.prediction_data.top_prediction;
                                else if (Array.isArray(pred.prediction_data.details) && pred.prediction_data.details.length > 0) {
                                    topRole = pred.prediction_data.details[0].role;
                                }
                            }

                            return (
                                <tr key={pred.id}>
                                    <td>{new Date(pred.timestamp).toLocaleDateString()}</td>
                                    <td>{pred.username || "Anonymous"}</td>
                                    <td>
                                        <span style={{ fontWeight: 600, color: '#4f46e5' }}>{topRole}</span>
                                    </td>
                                    {showUserFeedback && (
                                        <td>
                                            {pred.rating && (
                                                <div style={{ color: '#f59e0b', marginBottom: '4px' }}>
                                                    {'★'.repeat(pred.rating)}
                                                </div>
                                            )}
                                            {pred.feedback_text && (
                                                <div style={{ fontSize: '0.85rem', fontStyle: 'italic', color: '#4b5563', maxWidth: '300px', maxHeight: '100px', overflowY: 'auto', whiteSpace: 'normal', wordBreak: 'break-word', paddingRight: '5px' }}>
                                                    "{pred.feedback_text}"
                                                </div>
                                            )}
                                            {!pred.rating && !pred.feedback_text && <span style={{ color: '#9ca3af' }}>-</span>}
                                        </td>
                                    )}
                                    {showAdminFeedback && (
                                        <td>
                                            {pred.correction ? (
                                                <div style={{ fontSize: '0.9rem', color: '#1f2937', maxWidth: '300px', maxHeight: '100px', overflowY: 'auto', whiteSpace: 'normal', wordBreak: 'break-word', paddingRight: '5px' }}>{pred.correction}</div>
                                            ) : (
                                                <span style={{ color: '#9ca3af' }}>-</span>
                                            )}
                                        </td>
                                    )}
                                    <td>
                                        <span style={{
                                            padding: '4px 8px',
                                            borderRadius: '4px',
                                            fontSize: '0.75rem',
                                            fontWeight: 'bold',
                                            backgroundColor: pred.is_flagged ? '#fee2e2' : '#dcfce7',
                                            color: pred.is_flagged ? '#b91c1c' : '#15803d'
                                        }}>
                                            {pred.is_flagged ? 'Flagged' : 'Normal'}
                                        </span>
                                    </td>
                                    <td>
                                        <button
                                            onClick={() => handleFlag(pred.id, pred.is_flagged, pred.correction)}
                                            className={pred.is_flagged ? 'btn-flag btn-flag-active' : 'btn-flag btn-flag-inactive'}
                                        >
                                            {pred.is_flagged ? 'Resolve / Edit' : 'Flag'}
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            )}
        </div>
    );

    const renderUsersTable = () => (
        <div className="data-table-container">
            {users.length === 0 ? (
                <p style={{ padding: '20px', color: '#6b7280' }}>No users found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Date Joined</th>
                            <th>Role</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(u => (
                            <tr key={u.id}>
                                <td>{u.id}</td>
                                <td>{u.username}</td>
                                <td>{u.email}</td>
                                <td>
                                    {u.date_joined
                                        ? new Date(u.date_joined).toLocaleDateString()
                                        : <span className="text-gray-400 italic">Unknown</span>}
                                </td>
                                <td>
                                    {u.is_staff ? (
                                        <span style={{ background: '#dbeafe', color: '#1e40af', padding: '2px 8px', borderRadius: '10px', fontSize: '0.75em', fontWeight: 'bold' }}>Admin</span>
                                    ) : (
                                        <span style={{ background: '#f3f4f6', color: '#374151', padding: '2px 8px', borderRadius: '10px', fontSize: '0.75em' }}>User</span>
                                    )}
                                </td>
                                <td>
                                    {!u.is_staff && (
                                        <button
                                            onClick={() => handleDeleteUser(u.id)}
                                            className="btn-flag"
                                            style={{ background: '#fee2e2', color: '#b91c1c' }}
                                        >
                                            Delete
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );

    return (
        <div className="admin-dashboard">
            {/* Navbar */}
            <Header />
            <div className="dashboard-container">
                <div className="dashboard-header">
                    <h1 className="dashboard-title">Admin Dashboard</h1>
                    <p className="dashboard-subtitle">Manage predictions, view analytics, and monitor system health.</p>
                </div>

                {/* Stats Cards */}
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-title">Total Users</div>
                        <div className="stat-value">{stats.total_users}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-title">Total Predictions</div>
                        <div className="stat-value">{stats.total_predictions}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-title" style={{ color: '#ef4444' }}>Flagged Issues</div>
                        <div className="stat-value" style={{ color: '#ef4444' }}>{stats.flagged_predictions}</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-title" style={{ color: '#f59e0b' }}>User Reviews</div>
                        <div className="stat-value" style={{ color: '#f59e0b' }}>{userReviews.length}</div>
                    </div>
                </div>

                {/* Tabs */}
                <div className="tabs-container">
                    <button
                        className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        All Logs
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'users' ? 'active' : ''}`}
                        onClick={() => setActiveTab('users')}
                    >
                        Users
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'flagged' ? 'active' : ''}`}
                        onClick={() => setActiveTab('flagged')}
                    >
                        Flagged
                        {flaggedPredictions.length > 0 && <span style={{ marginLeft: '8px', background: '#fee2e2', color: '#b91c1c', padding: '2px 6px', borderRadius: '10px', fontSize: '0.7em' }}>{flaggedPredictions.length}</span>}
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'reviews' ? 'active' : ''}`}
                        onClick={() => setActiveTab('reviews')}
                    >
                        Reviews
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'corrections' ? 'active' : ''}`}
                        onClick={() => setActiveTab('corrections')}
                    >
                        Corrections
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'settings' ? 'active' : ''}`}
                        onClick={() => setActiveTab('settings')}
                    >
                        Settings
                    </button>
                </div>

                {/* Tab Content */}
                <div className="tab-content">
                    {activeTab === 'overview' && (
                        <div className="section-card">
                            <div className="section-header">
                                <h3 className="section-title">All Prediction Logs</h3>
                            </div>
                            {renderTable(predictions)}
                        </div>
                    )}

                    {activeTab === 'users' && (
                        <div className="section-card">
                            <div className="section-header">
                                <h3 className="section-title">User Management</h3>
                            </div>
                            {renderUsersTable()}
                        </div>
                    )}

                    {activeTab === 'flagged' && (
                        <div className="section-card">
                            <div className="section-header">
                                <h3 className="section-title" style={{ color: '#ef4444' }}>Flagged Predictions</h3>
                            </div>
                            {renderTable(flaggedPredictions, true, true)}
                        </div>
                    )}

                    {activeTab === 'reviews' && (
                        <div className="section-card">
                            <div className="section-header">
                                <h3 className="section-title">User Feedback & Ratings</h3>
                            </div>
                            {renderTable(userReviews, true, false)}
                        </div>
                    )}

                    {activeTab === 'corrections' && (
                        <div className="section-card">
                            <div className="section-header">
                                <h3 className="section-title">Admin Feedback History</h3>
                            </div>
                            {renderTable(adminCorrections, false, true)}
                        </div>
                    )}

                    {activeTab === 'settings' && (
                        <div className="section-card" style={{ padding: '30px' }}>
                            <h3 className="section-title" style={{ marginBottom: '20px' }}>System Settings & Model</h3>

                            <div style={{ marginBottom: '30px' }}>
                                <h4 style={{ marginBottom: '15px', color: '#374151' }}>Fine-tuning / Retraining</h4>
                                <p style={{ color: '#4b5563', marginBottom: '15px', maxWidth: '600px', fontSize: '0.95em' }}>
                                    Upload a new CSV dataset to retrain the Random Forest model, or simply retrain using the existing dataset.
                                    You can specifically choose to include <strong>User Feedback (4+ Stars)</strong> and <strong>Admin Corrections</strong> to improve the model.
                                </p>

                                <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center' }}>
                                    <input
                                        type="checkbox"
                                        id="feedbackCheckbox"
                                        checked={includeFeedback}
                                        onChange={(e) => setIncludeFeedback(e.target.checked)}
                                        style={{ width: '18px', height: '18px', marginRight: '10px', cursor: 'pointer' }}
                                    />
                                    <label htmlFor="feedbackCheckbox" style={{ cursor: 'pointer', fontWeight: 500, color: '#1f2937' }}>
                                        Include High-Rated Feedback & Admin Corrections in Training Data
                                    </label>
                                </div>

                                <div style={{ display: 'flex', gap: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
                                    <input
                                        type="file"
                                        accept=".csv"
                                        onChange={handleFileChange}
                                        style={{ padding: '10px', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                                    />

                                    <button
                                        onClick={handleRetrain}
                                        className="btn-flag"
                                        style={{
                                            background: '#2563eb',
                                            color: 'white',
                                            padding: '12px 24px',
                                            fontSize: '1rem',
                                            opacity: (!file && !includeFeedback) ? 0.8 : 1,
                                            cursor: 'pointer'
                                        }}
                                    >
                                        Retrain Model
                                    </button>
                                </div>

                                {retrainMsg && (
                                    <div style={{ marginTop: '20px', padding: '15px', background: '#f3f4f6', borderRadius: '8px', color: '#1f2937' }}>
                                        {retrainMsg}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
