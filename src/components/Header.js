import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import logo from '../assets/logo.png'; // Add your logo to assets folder

const Header = () => {
    const navigate = useNavigate();
    const user = authService.getCurrentUser();
    
    const handleLogout = () => {
        authService.logout();
        navigate('/login');
    };
    
    return (
        <header className="header">
            <div className="logo-section">
                <img src={logo} alt="Company Logo" className="logo" />
                <h1 className="company-name">Accounting System</h1>
            </div>
            
            {user && (
                <div className="user-section">
                    <div className="user-info">
                        <div className="user-name">
                            {user.first_name} {user.last_name}
                        </div>
                        <div className="user-role">
                            {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                        </div>
                    </div>
                    
                    {user.profile_picture ? (
                        <img 
                            src={user.profile_picture} 
                            alt={`${user.first_name} ${user.last_name}`} 
                            className="profile-picture" 
                        />
                    ) : (
                        <div className="profile-initial">
                            {user.first_name.charAt(0).toUpperCase()}
                        </div>
                    )}
                    
                    <button className="logout-button" onClick={handleLogout}>
                        Logout
                    </button>
                </div>
            )}
            
            <style jsx>{`
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px 30px;
                    background-color: white;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                
                .logo-section {
                    display: flex;
                    align-items: center;
                }
                
                .logo {
                    height: 40px;
                    width: auto;
                    margin-right: 15px;
                }
                
                .company-name {
                    font-size: 20px;
                    font-weight: 600;
                    color: #333;
                    margin: 0;
                }
                
                .user-section {
                    display: flex;
                    align-items: center;
                }
                
                .user-info {
                    text-align: right;
                    margin-right: 15px;
                }
                
                .user-name {
                    font-weight: 600;
                    margin-bottom: 2px;
                }
                
                .user-role {
                    font-size: 14px;
                    color: #666;
                }
                
                .profile-picture {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin-right: 15px;
                }
                
                .profile-initial {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background-color: #4a6fdc;
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-weight: 600;
                    font-size: 18px;
                    margin-right: 15px;
                }
                
                .logout-button {
                    padding: 8px 16px;
                    background-color: #f5f5f5;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .logout-button:hover {
                    background-color: #e5e5e5;
                }
            `}</style>
        </header>
    );
};

export default Header;