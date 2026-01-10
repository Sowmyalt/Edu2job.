import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    let [user, setUser] = useState(() => localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')) : null);
    let [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    let loginUser = async (e, redirectPath = '/dashboard') => {
        if (e && e.preventDefault) e.preventDefault();
        try {
            const response = await api.post('login/', {
                username: e.target.username.value,
                password: e.target.password.value
            });

            if (response.status === 200) {
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                setUser(jwtDecode(response.data.access));
                navigate(redirectPath);
            }
        } catch (error) {
            alert('Something went wrong!');
        }
    };

    let googleLogin = async (tokenResponse) => {
        try {
            // In real app, exchange this token with backend
            const response = await api.post('google/', {
                token: tokenResponse.credential, // or access_token depending on flow
                email: jwtDecode(tokenResponse.credential).email // Helper for placeholder backend
            });

            if (response.data.access) {
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                setUser(jwtDecode(response.data.access));
                navigate('/dashboard');
            }
        } catch (error) {
            console.error("Google Login Error:", error);
            const msg = error.response?.data?.error || error.message || "Unknown Error";
            alert('Google Login Failed: ' + msg);
        }
    }

    let logoutUser = () => {
        setUser(null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };

    // Add context data here
    let contextData = {
        user: user,
        loginUser: loginUser,
        logoutUser: logoutUser,
        googleLogin: googleLogin,
    };

    useEffect(() => {
        // Could verify token here
        setLoading(false);
    }, []);

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
};
