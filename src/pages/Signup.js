import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import logo from '../assets/logo.png'; // Add your logo to assets folder

const Signup = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        address: '',
        date_of_birth: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            const response = await authService.register(formData);
            setSuccess('Registration request submitted successfully. You will receive an email once an administrator approves your request.');
            
            // Clear form
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                address: '',
                date_of_birth: ''
            });
            
            // Redirect to login after a delay
            setTimeout(() => {
                navigate('/login');
            }, 5000);
        } catch (err) {
            setError(err.message || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="signup-container">
            <div className="signup-box">
                <div className="logo-container">
                    <img src={logo} alt="Company Logo" className="logo" />
                </div>
                <h2>Request New Account</h2>
                
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">{success}</div>}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="first_name">First Name*</label>
                        <input
                            type="text"
                            id="first_name"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                            required
                            className="form-control"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="last_name">Last Name*</label>
                        <input
                            type="text"
                            id="last_name"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                            required
                            className="form-control"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="email">Email Address*</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className="form-control"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="address">Address</label>
                        <input
                            type="text"
                            id="address"
                            name="address"
                            value={formData.address}
                            onChange={handleChange}
                            className="form-control"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="date_of_birth">Date of Birth</label>
                        <input
                            type="date"
                            id="date_of_birth"
                            name="date_of_birth"
                            value={formData.date_of_birth}
                            onChange={handleChange}
                            className="form-control"
                        />
                    </div>
                    
                    <button 
                        type="submit" 
                        className="btn btn-primary btn-block"
                        disabled={loading}
                    >
                        {loading ? 'Submitting...' : 'Submit Request'}
                    </button>
                    
                    <div className="links-container">
                        <Link to="/login" className="link">
                            Back to Login
                        </Link>
                    </div>
                </form>
            </div>
            
            <style jsx>{`
                .signup-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background-color: #f5f5f5;
                    padding: 20px;
                }
                
                .signup-box {
                    width: 500px;
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

export default Signup;