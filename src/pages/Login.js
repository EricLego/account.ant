import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../services/authService';
import logo from '../assets/logo.png'; // Add your logo to assets folder

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        // Redirect if already logged in
        if (authService.isAuthenticated()) {
            navigate('/dashboard');
        }
    }, [navigate]);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await authService.login(username, password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.message || 'Failed to login. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="logo-container">
                    <img src={logo} alt="Company Logo" className="logo" />
                </div>
                <h2>Accounting System Login</h2>
                
                {error && <div className="error-message">{error}</div>}
                
                <form onSubmit={handleLogin}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            className="form-control"
                            placeholder="Enter your username"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="form-control"
                            placeholder="Enter your password"
                        />
                    </div>
                    
                    <button 
                        type="submit" 
                        className="btn btn-primary btn-block"
                        disabled={loading}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                    
                    <div className="links-container">
                        <Link to="/forgot-password" className="link">
                            Forgot Password?
                        </Link>
                        <Link to="/signup" className="link">
                            Create New Account
                        </Link>
                    </div>
                </form>
            </div>
            
            <style jsx>{`
                .login-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background-color: #f5f5f5;
                }
                
                .login-box {
                    width: 400px;
                    padding: 40px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                }
                
                .logo-container {
                    text-align: center;
                    margin-bottom: 20px;
                }
                
                .logo {
                    max-width: 150px;
                    height: auto;
                }
                
                h2 {
                    text-align: center;
                    margin-bottom: 30px;
                    color: #333;
                }
                
                .form-group {
                    margin-bottom: 20px;
                }
                
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: 500;
                }
                
                .form-control {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                
                .btn {
                    width: 100%;
                    padding: 12px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    margin-top: 10px;
                }
                
                .btn-primary {
                    background-color: #4a6fdc;
                    color: white;
                }
                
                .btn-primary:hover {
                    background-color: #3a5dca;
                }
                
                .btn:disabled {
                    background-color: #b3b3b3;
                    cursor: not-allowed;
                }
                
                .error-message {
                    background-color: #ffebee;
                    color: #d32f2f;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                
                .links-container {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 20px;
                }
                
                .link {
                    color: #4a6fdc;
                    text-decoration: none;
                }
                
                .link:hover {
                    text-decoration: underline;
                }
            `}</style>
        </div>
    );
};

export default Login;