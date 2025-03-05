from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import datetime
import uuid
import pyodbc
from routes.auth import token_required, get_db_connection, validate_password

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/list', methods=['GET'])
@token_required
def list_users(current_user):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, first_name, last_name, email, role, active, suspended_until, last_login, created_at FROM users')
    
    user_list = []
    for row in cursor.fetchall():
        user_dict = {
            'id': row.id,
            'username': row.username,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'email': row.email,
            'role': row.role,
            'active': row.active,
            'suspended_until': row.suspended_until.isoformat() if row.suspended_until else None,
            'last_login': row.last_login.isoformat() if row.last_login else None,
            'created_at': row.created_at.isoformat() if row.created_at else None
        }
        user_list.append(user_dict)
    
    conn.close()
    
    return jsonify({'users': user_list}), 200

@user_bp.route('/user/create', methods=['POST'])
@token_required
def create_user(current_user):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Validate role
    if data['role'] not in ['administrator', 'manager', 'accountant']:
        return jsonify({'message': 'Invalid role. Must be administrator, manager, or accountant'}), 400
    
    conn = get_db_connection()
    
    # Check if email already exists
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({'message': 'Email already in use'}), 400
    
    # Generate username
    now = datetime.datetime.utcnow()
    username = f"{data['first_name'][0].lower()}{data['last_name'].lower()}{now.strftime('%m%y')}"
    
    # Check if username exists and add a number if it does
    count = 1
    original_username = username
    while True:
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if not existing:
            break
        username = f"{original_username}{count}"
        count += 1
    
    # Generate temporary password
    temp_password = f"{data['first_name'][0].upper()}{data['last_name'][0].lower()}!{uuid.uuid4().hex[:6]}"
    
    # Validate password
    valid, message = validate_password(temp_password)
    if not valid:
        # This should not happen with our password generation scheme, but just in case
        temp_password = "Temp123!456"
    
    hashed_password = generate_password_hash(temp_password)
    
    # Create user
    user_id = str(uuid.uuid4())
    now_iso = datetime.datetime.utcnow().isoformat()
    
    conn.execute(
        '''INSERT INTO users 
           (id, username, password, first_name, last_name, email, role, active, created_at, address, date_of_birth, profile_picture)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, username, hashed_password, data['first_name'], data['last_name'], data['email'], 
         data['role'], 1, now_iso, data.get('address'), data.get('date_of_birth'), data.get('profile_picture'))
    )
    
    # Add to password history
    conn.execute(
        'INSERT INTO password_history (id, user_id, password, created_at) VALUES (?, ?, ?, ?)',
        (str(uuid.uuid4()), user_id, hashed_password, now_iso)
    )
    
    conn.commit()
    conn.close()
    
    # TODO: Send email with temporary credentials
    
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': user_id,
            'username': username,
            'temporary_password': temp_password  # In production, would only send via email
        }
    }), 201

@user_bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if current_user['role'] != 'administrator' and current_user['id'] != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    user = conn.execute('SELECT id, username, first_name, last_name, email, role, active, suspended_until, last_login, created_at, address, date_of_birth, profile_picture FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'user': dict(user)}), 200

@user_bp.route('/user/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    # Fields that can be updated
    updatable_fields = ['first_name', 'last_name', 'email', 'role', 'address', 'date_of_birth', 'profile_picture']
    
    # Build SQL update statement
    update_fields = []
    params = []
    
    for field in updatable_fields:
        if field in data:
            update_fields.append(f"{field} = ?")
            params.append(data[field])
    
    if not update_fields:
        conn.close()
        return jsonify({'message': 'No fields to update'}), 400
    
    # Add user_id to params
    params.append(user_id)
    
    # Execute update
    conn.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?", params)
    conn.commit()
    
    # Get updated user
    updated_user = conn.execute('SELECT id, username, first_name, last_name, email, role, active, suspended_until, last_login, created_at, address, date_of_birth, profile_picture FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': dict(updated_user)
    }), 200

@user_bp.route('/user/<user_id>/activate', methods=['POST'])
@token_required
def activate_user(current_user, user_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    conn.execute('UPDATE users SET active = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User activated successfully'}), 200

@user_bp.route('/user/<user_id>/deactivate', methods=['POST'])
@token_required
def deactivate_user(current_user, user_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Don't allow deactivating self
    if current_user['id'] == user_id:
        return jsonify({'message': 'Cannot deactivate yourself'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    conn.execute('UPDATE users SET active = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User deactivated successfully'}), 200

@user_bp.route('/user/<user_id>/suspend', methods=['POST'])
@token_required
def suspend_user(current_user, user_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Don't allow suspending self
    if current_user['id'] == user_id:
        return jsonify({'message': 'Cannot suspend yourself'}), 400
    
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not end_date:
        return jsonify({'message': 'Missing end date for suspension'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    # If start_date not provided, use current time
    if not start_date:
        start_date = datetime.datetime.utcnow().isoformat()
    
    conn.execute('UPDATE users SET suspended_until = ? WHERE id = ?', (end_date, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User suspended successfully'}), 200

@user_bp.route('/user/<user_id>/unsuspend', methods=['POST'])
@token_required
def unsuspend_user(current_user, user_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404
    
    conn.execute('UPDATE users SET suspended_until = NULL WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User unsuspended successfully'}), 200

@user_bp.route('/user/expired-passwords', methods=['GET'])
@token_required
def list_expired_passwords(current_user):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    
    # Join users and password_history to get the latest password change date for each user
    query = '''
    SELECT u.id, u.username, u.first_name, u.last_name, u.email, ph.created_at as password_date
    FROM users u
    JOIN (
        SELECT user_id, MAX(created_at) as created_at
        FROM password_history
        GROUP BY user_id
    ) ph ON u.id = ph.user_id
    WHERE u.active = 1
    '''
    
    users = conn.execute(query).fetchall()
    conn.close()
    
    expired_users = []
    for user in users:
        password_date = datetime.datetime.fromisoformat(user['password_date'])
        days_since_change = (datetime.datetime.utcnow() - password_date).days
        
        if days_since_change > 90:  # Password expired (90 days)
            user_dict = dict(user)
            user_dict['days_since_change'] = days_since_change
            expired_users.append(user_dict)
    
    return jsonify({'expired_passwords': expired_users}), 200

@user_bp.route('/user/registration-requests', methods=['GET'])
@token_required
def list_registration_requests(current_user):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM registration_requests WHERE status = "pending"').fetchall()
    conn.close()
    
    request_list = [dict(req) for req in requests]
    
    return jsonify({'registration_requests': request_list}), 200

@user_bp.route('/user/approve-registration/<request_id>', methods=['POST'])
@token_required
def approve_registration(current_user, request_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    registration = conn.execute('SELECT * FROM registration_requests WHERE id = ?', (request_id,)).fetchone()
    
    if not registration:
        conn.close()
        return jsonify({'message': 'Registration request not found'}), 404
    
    if registration['status'] != 'pending':
        conn.close()
        return jsonify({'message': f'Registration already {registration["status"]}'}), 400
    
    # Generate username based on first initial, last name, and date
    now = datetime.datetime.utcnow()
    username = f"{registration['first_name'][0].lower()}{registration['last_name'].lower()}{now.strftime('%m%y')}"
    
    # Check if username exists and add a number if it does
    count = 1
    original_username = username
    while True:
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if not existing:
            break
        username = f"{original_username}{count}"
        count += 1
    
    # Generate a temporary password
    temp_password = f"{registration['first_name'][0].upper()}{registration['last_name'][0].lower()}!{uuid.uuid4().hex[:6]}"
    hashed_password = generate_password_hash(temp_password)
    
    # Create user
    user_id = str(uuid.uuid4())
    now_iso = now.isoformat()
    
    conn.execute(
        '''INSERT INTO users 
           (id, username, password, first_name, last_name, email, role, active, created_at, address, date_of_birth)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, username, hashed_password, registration['first_name'], registration['last_name'], 
         registration['email'], 'accountant', 1, now_iso, registration['address'], registration['date_of_birth'])
    )
    
    # Add to password history
    conn.execute(
        'INSERT INTO password_history (id, user_id, password, created_at) VALUES (?, ?, ?, ?)',
        (str(uuid.uuid4()), user_id, hashed_password, now_iso)
    )
    
    # Update registration request
    conn.execute('UPDATE registration_requests SET status = ? WHERE id = ?', ('approved', request_id))
    
    conn.commit()
    conn.close()
    
    # TODO: Send email with temporary credentials
    
    return jsonify({
        'message': 'Registration approved',
        'username': username,
        'temporary_password': temp_password  # In production, would only send via email
    }), 200

@user_bp.route('/user/reject-registration/<request_id>', methods=['POST'])
@token_required
def reject_registration(current_user, request_id):
    if current_user['role'] != 'administrator':
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    reason = data.get('reason', 'No reason provided')
    
    conn = get_db_connection()
    registration = conn.execute('SELECT * FROM registration_requests WHERE id = ?', (request_id,)).fetchone()
    
    if not registration:
        conn.close()
        return jsonify({'message': 'Registration request not found'}), 404
    
    if registration['status'] != 'pending':
        conn.close()
        return jsonify({'message': f'Registration already {registration["status"]}'}), 400
    
    # Update registration request
    conn.execute('UPDATE registration_requests SET status = ? WHERE id = ?', ('rejected', request_id))
    conn.commit()
    conn.close()
    
    # TODO: Send rejection email
    
    return jsonify({'message': 'Registration rejected'}), 200