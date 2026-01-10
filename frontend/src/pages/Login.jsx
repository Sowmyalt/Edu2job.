import { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import { GoogleLogin } from '@react-oauth/google';

const Login = ({ isAdmin = false }) => {
    let { loginUser, googleLogin } = useContext(AuthContext);

    const handleSubmit = (e) => {
        loginUser(e, isAdmin ? '/admin' : '/dashboard');
    }

    return (
        <div className={`min-h-screen flex justify-center items-center font-sans relative overflow-hidden ${isAdmin ? 'bg-gradient-to-br from-gray-800 to-black' : 'bg-gradient-to-br from-blue-600 to-purple-700'}`}>
            <div className="absolute inset-0 bg-white/10 backdrop-blur-[2px]" />

            <div className="bg-white/90 backdrop-blur-md p-10 rounded-sm shadow-2xl w-96 relative z-10 border border-white/20">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-800 tracking-tight">{isAdmin ? 'Admin Portal' : 'Welcome Back'}</h1>
                    <p className="text-gray-500 text-sm mt-2">{isAdmin ? 'Authorized Personnel Only' : 'Sign in to continue your journey'}</p>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="mb-8 relative">
                        <input
                            type="text"
                            name="username"
                            className="w-full py-2 border-b-2 border-gray-300 focus:border-blue-500 outline-none text-gray-700 bg-transparent peer placeholder-transparent transition-colors"
                            placeholder="Username"
                            required
                        />
                        <label className="absolute left-0 -top-3.5 text-gray-500 text-sm transition-all 
                                        peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 
                                        peer-placeholder-shown:top-2 peer-focus:-top-3.5 peer-focus:text-gray-500 peer-focus:text-sm">
                            Username
                        </label>
                    </div>

                    <div className="mb-8 relative">
                        <input
                            type="password"
                            name="password"
                            className="w-full py-2 border-b-2 border-gray-300 focus:border-blue-500 outline-none text-gray-700 bg-transparent peer placeholder-transparent transition-colors"
                            placeholder="Password"
                            required
                        />
                        <label className="absolute left-0 -top-3.5 text-gray-500 text-sm transition-all 
                                        peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 
                                        peer-placeholder-shown:top-2 peer-focus:-top-3.5 peer-focus:text-gray-500 peer-focus:text-sm">
                            Password
                        </label>
                    </div>

                    <div className="flex justify-between items-center mb-8">
                        <span className="text-gray-400 text-sm hover:text-blue-500 cursor-pointer transition-colors">Forgot Password?</span>
                    </div>

                    <button
                        type="submit"
                        className="w-full text-white font-bold py-3 rounded-sm shadow-md uppercase tracking-wide hover:scale-105 transition-transform"
                        style={{ background: isAdmin ? 'linear-gradient(to right, #1f2937, #000000)' : 'var(--blue-gradient)' }}
                    >
                        {isAdmin ? 'Login as Admin' : 'Login'}
                    </button>

                    <div className="mt-6 flex justify-center">
                        <GoogleLogin
                            onSuccess={googleLogin}
                            onError={() => console.log('Login Failed')}
                            type="icon"
                            shape="circle"
                            theme="filled_blue"
                        />
                    </div>
                </form>

                <p className="mt-8 text-center text-sm text-gray-500">
                    {isAdmin ? (
                        <>
                            Not an admin? <Link to="/login" className="text-blue-500 font-semibold hover:underline">User Login</Link>
                        </>
                    ) : (
                        <>
                            Not a member? <Link to="/register" className="text-blue-500 font-semibold hover:underline">Signup</Link>
                            <br />
                            <Link to="/admin/login" className="text-gray-400 text-xs hover:text-gray-600 mt-2 inline-block">Are you an admin?</Link>
                        </>
                    )}
                </p>
            </div>
        </div>
    );
};

export default Login;
