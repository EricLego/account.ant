import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import authService from '../services/authService';
import logo from '../assets/logo.png'; // Add your logo to assets folder

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            await authService.forgotPassword(email, username);
            setSuccess('Password reset instructions have been sent to your email.');
            
            // Clear form
            setEmail('');
            setUsername('');
        } catch (err) {
            setError(err.message || 'Failed to process request. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="forgot-password-container">
            <div className="forgot-password-box">
                <div className="logo-container">
                    <img src={logo} alt="Company Logo" className="logo" />
                </div>
                <h2>Reset Password</h2>
                
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">{success}</div>}
                
                <p className="instruction">
                    Please enter your email address and username to receive password reset instructions.
                </p>
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="form-control"
                            placeholder="Enter your email"
                        />
                    </div>
                    
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
                    
                    <button 
                        type="submit" 
                        className="btn btn-primary btn-block"
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : 'Reset Password'}
                    </button>
                    
                    <div className="links-container">
                        <Link to="/login" className="link">
                            Back to Login
                        </Link>
                    </div>
                </form>
            </div>
            
            <style jsx>{`
                .forgot-password-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background-color: #f5f5f5;
                }
                
                .forgot-password-box {
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
                    margin-bottom: 20px;
                    color: #333;
                }
                
                .instruction {
                    margin-bottom: 30px;
                    text-align: center;
                    color: #666;
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
                
                .success-message {
                    background-color: #e8f5e9;
                    color: #2e7d32;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                
                .links-container {
                    display: flex;
                    justify-content: center;
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

export default ForgotPassword;