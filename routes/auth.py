from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import uuid
from functools import wraps
import re
import os
import pyodbc
import dotenv

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

auth_bp = Blueprint('auth', __name__)

# Database connection
CONNECTION_STRING = "Server=tcp:account-ant.database.windows.net,1433;Initial Catalog=account-ant-employee;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;Authentication=SqlPassword;UID=workerAnt;PWD=forTheColony01!!"

def get_db_connection():
    conn = pyodbc.connect(CONNECTION_STRING)
    return conn

# Initialize database tables if they don't exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if Users table exists
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
    BEGIN
        CREATE TABLE users (
            id NVARCHAR(36) PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            password NVARCHAR(255) NOT NULL,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            role NVARCHAR(20) NOT NULL,
            active BIT NOT NULL DEFAULT 1,
            suspended_until DATETIME,
            failed_attempts INT NOT NULL DEFAULT 0,
            last_login DATETIME,
            created_at DATETIME NOT NULL,
            profile_picture NVARCHAR(255),
            address NVARCHAR(255),
            date_of_birth DATE
        )
    END
    """)
    
    # Check if Password history table exists
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'password_history')
    BEGIN
        CREATE TABLE password_history (
            id NVARCHAR(36) PRIMARY KEY,
            user_id NVARCHAR(36) NOT NULL,
            password NVARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    END
    """)
    
    # Check if Registration requests table exists
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'registration_requests')
    BEGIN
        CREATE TABLE registration_requests (
            id NVARCHAR(36) PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            address NVARCHAR(255),
            date_of_birth DATE,
            created_at DATETIME NOT NULL,
            status NVARCHAR(20) NOT NULL
        )
    END
    """)
    
    # Create default admin user if no users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    row = cursor.fetchone()
    if row[0] == 0:
        admin_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow()
        admin_password = generate_password_hash('Admin123!')
        
        cursor.execute(
            """INSERT INTO users 
               (id, username, password, first_name, last_name, email, role, active, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (admin_id, 'aadmin0322', admin_password, 'Admin', 'User', 'admin@example.com', 'administrator', 1, now)
        )
        
        # Add password to history
        password_history_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO password_history 
               (id, user_id, password, created_at) 
               VALUES (?, ?, ?, ?)""",
            (password_history_id, admin_id, admin_password, now)
        )
    
    conn.commit()
    conn.close()

# Call initialization
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization error: {str(e)}")

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (data['sub'],))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return jsonify({'message': 'User not found'}), 401
            
            # Convert user to dictionary
            user_dict = {
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'active': user.active,
                'suspended_until': user.suspended_until,
                'failed_attempts': user.failed_attempts,
                'last_login': user.last_login,
                'created_at': user.created_at,
                'profile_picture': user.profile_picture,
                'address': user.address,
                'date_of_birth': user.date_of_birth
            }
            
            conn.close()
                
            if not user_dict['active']:
                return jsonify({'message': 'Account is deactivated'}), 403
                
            # Check if user is suspended
            if user_dict['suspended_until'] and user_dict['suspended_until'] > datetime.datetime.utcnow():
                return jsonify({'message': 'Account is suspended'}), 403
                
        except Exception as e:
            return jsonify({'message': f'Token is invalid: {str(e)}'}), 401
            
        return f(user_dict, *args, **kwargs)
    
    return decorated

# Password validation
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not password[0].isalpha():
        return False, "Password must start with a letter"
    
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

# Check if password was used before
def password_used_before(user_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT TOP 5 password FROM password_history WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    password_history = cursor.fetchall()
    conn.close()
    
    for old_password in password_history:
        if check_password_hash(old_password[0], password):
            return True
    
    return False

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Convert user to dictionary
    user_dict = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
        'active': user.active,
        'suspended_until': user.suspended_until,
        'failed_attempts': user.failed_attempts,
        'last_login': user.last_login,
        'created_at': user.created_at,
        'profile_picture': user.profile_picture
    }
    
    if not user_dict['active']:
        conn.close()
        return jsonify({'message': 'Account is deactivated'}), 403
    
    # Check if user is suspended
    if user_dict['suspended_until'] and user_dict['suspended_until'] > datetime.datetime.utcnow():
        conn.close()
        return jsonify({'message': 'Account is suspended'}), 403
    
    if not check_password_hash(user_dict['password'], password):
        # Increment failed attempts
        failed_attempts = user_dict['failed_attempts'] + 1
        
        if failed_attempts >= 3:
            # Suspend account for 24 hours
            suspended_until = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            cursor.execute('UPDATE users SET failed_attempts = ?, suspended_until = ? WHERE id = ?', 
                        (failed_attempts, suspended_until, user_dict['id']))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Account locked due to too many failed attempts'}), 403
        else:
            cursor.execute('UPDATE users SET failed_attempts = ? WHERE id = ?', (failed_attempts, user_dict['id']))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Invalid username or password'}), 401
    
    # Reset failed attempts and update last login
    now = datetime.datetime.utcnow()
    cursor.execute('UPDATE users SET failed_attempts = 0, last_login = ? WHERE id = ?', (now, user_dict['id']))
    conn.commit()
    
    # Check if password is about to expire (90 days)
    cursor.execute('SELECT TOP 1 created_at FROM password_history WHERE user_id = ? ORDER BY created_at DESC', 
                 (user_dict['id'],))
    latest_password = cursor.fetchone()
    
    password_expiring = False
    if latest_password:
        password_date = latest_password[0]
        days_to_expiration = 90 - (datetime.datetime.utcnow() - password_date).days
        
        if 0 <= days_to_expiration <= 3:
            password_expiring = True
    
    conn.close()
    
    # Generate token
    token = jwt.encode({
        'sub': user_dict['id'],
        'username': user_dict['username'],
        'role': user_dict['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, 'your-secret-key', algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user_dict['id'],
            'username': user_dict['username'],
            'first_name': user_dict['first_name'],
            'last_name': user_dict['last_name'],
            'email': user_dict['email'],
            'role': user_dict['role'],
            'profile_picture': user_dict['profile_picture'],
            'password_expiring': password_expiring
        }
    }), 200

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    address = data.get('address')
    date_of_birth = data.get('date_of_birth')
    
    if not first_name or not last_name or not email:
        return jsonify({'message': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists in registration requests
    cursor.execute('SELECT * FROM registration_requests WHERE email = ?', (email,))
    existing_request = cursor.fetchone()
    
    # Check if email already exists in users
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    
    if existing_request or existing_user:
        conn.close()
        return jsonify({'message': 'Email already registered'}), 400
    
    request_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow()
    
    # Convert date_of_birth to date object if provided
    birth_date = None
    if date_of_birth:
        try:
            birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    cursor.execute(
        '''INSERT INTO registration_requests 
           (id, first_name, last_name, email, address, date_of_birth, created_at, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (request_id, first_name, last_name, email, address, birth_date, now, 'pending')
    )
    conn.commit()
    conn.close()
    
    # TODO: Send email notification to administrator
    
    return jsonify({'message': 'Registration request submitted', 'request_id': request_id}), 201

@auth_bp.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    
    if not email or not username:
        return jsonify({'message': 'Missing email or username'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND username = ?', (email, username))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    # TODO: Implement security questions
    # TODO: Send password reset email
    
    conn.close()
    return jsonify({'message': 'Password reset instructions sent to email'}), 200

@auth_bp.route('/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'message': 'Missing old or new password'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (current_user['id'],))
    user = cursor.fetchone()
    
    if not check_password_hash(user.password, old_password):
        conn.close()
        return jsonify({'message': 'Old password is incorrect'}), 400
    
    # Validate new password
    valid, message = validate_password(new_password)
    if not valid:
        conn.close()
        return jsonify({'message': message}), 400
    
    # Check if password was used before
    if password_used_before(current_user['id'], new_password):
        conn.close()
        return jsonify({'message': 'Password was used before'}), 400
    
    # Update password
    hashed_password = generate_password_hash(new_password)
    now = datetime.datetime.utcnow()
    
    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, current_user['id']))
    
    # Add to password history
    password_history_id = str(uuid.uuid4())
    cursor.execute(
        '''INSERT INTO password_history 
           (id, user_id, password, created_at) 
           VALUES (?, ?, ?, ?)''',
        (password_history_id, current_user['id'], hashed_password, now)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Password updated successfully'}), 200