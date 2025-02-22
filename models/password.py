import pyodbc;
import jwt;
from passlib.context import CryptContext;
from datetime import date, datetime, timedelta, timezone;

# Much of this script is based on the one on this page: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

class Token:
    access_token: str
    refresh_token: str
    token_type: str

# Establish DB connection
cnxnStr = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:account-ant.database.windows.net,1433;Database=account-ant-employee;Uid=workerAnt;Pwd=forTheColony01!!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

cnxn = pyodbc.connect(cnxnStr)

cursor = cnxn.cursor()

# Encryption details
SECRET_KEY = "8bb273198502d80891729dc170355c31"
REFRESH_SECRET_KEY = "c473010cc73ad307721ca2736385c61c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 30

# Create encryption context
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Functions
def verify_password(plain, hashed):
    return pass_context.verify(plain, hashed)

def hash_pass(plain):
    return pass_context.hash(plain)

def get_user(username: str):
    cursor.execute(f"SELECT * FROM Users WHERE Username='{username}'")
    login_row = cursor.fetchone()

    # check if retrieval was successful
    if login_row == None:
        return False
    else:
        return login_row

def auth_user(username: str, password: str):
    user = get_user(cursor, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_token(data: dict, secret, lifetime: timedelta):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + lifetime
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, secret, algorithm=ALGORITHM)
    return encoded_jwt

def login(form_data):
    # Authenticate user
    user = auth_user(form_data.username, form_data.password)

    if not user:
        # User doesn't exist, create error message
        print("TO BE IMPLEMENTED")
    elif user.status == 1:
        # User currently suspended, create error message
        print("TO BE IMPLEMENTED")
    else:
        # Check for expired password
        cursor.execute(f"SELECT * FROM Passwords WHERE user_id='{user.user_id}'")
        pass_row = cursor.fetchone()
        
        if pass_row == None:
            # Password table doesn't contain user, create error message
            print("TO BE IMPLEMENTED")
        else:
            # Convert SQL date to Python date
            exp_date = date.fromisoformat(pass_row.expiry_date)
            if exp_date > datetime.now(timezone.utc).date():
                # Password has expired, create error message
                print("TO BE IMPLEMENTED")
            else:
                # Create access token
                new_access_token = create_token(
                    data={"sub": user.username, "type":"access"}, secret=SECRET_KEY, lifetime=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )

                # Hash and store access token
                hashed_access_token = pass_context.hash(new_access_token)
                cursor.execute(f"INSERT INTO Access_Tokens (user_id, token_hash, creation_time, expiry_time) VALUES ('{user.user_id}','{hashed_access_token}','{datetime.now(timezone.utc)}','{datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}')")

                # Create refresh token
                new_refresh_token = create_token(
                    data={"sub": user.username, "type":"refresh"}, secret=REFRESH_SECRET_KEY, lifetime=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
                )
                
                # Hash and store refresh token
                hashed_refresh_token = pass_context.hash(new_refresh_token)
                cursor.execute(f"INSERT INTO Refresh_Tokens (user_id, token_hash, creation_time, expiry_time) VALUES ('{user.user_id}','{hashed_refresh_token}','{datetime.now(timezone.utc)}','{datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)}')")

                return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
    
def auth_access_token(token):
    # Check if token is in DB
    cursor.execute(f"SELECT * FROM Access_Tokens WHERE token_hash='{token}'")
    token_row = cursor.fetchone()

    if token_row == None:
        return False
    
    decoded_jwt = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
    if decoded_jwt["exp"] > datetime.now(timezone.utc):
        return False
    
    return True
    
def auth_refresh_token(token):
    # Check if token is in DB
    cursor.execute(f"SELECT * FROM Refresh_Tokens WHERE token_hash='{token}'")
    token_row = cursor.fetchone()

    if token_row == None:
        return False
    
    decoded_jwt = jwt.decode(token, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    if decoded_jwt["exp"] > datetime.now(timezone.utc):
        return False
    
    return True

def update_pass(user_id, new_pass):
    # Retrieve list of past passwords
    cursor.execute(f"SELECT * FROM Passwords WHERE user_id='{user_id}'")
    pass_row = cursor.fetchone()

    if pass_row == None:
        # Given user doesn't exist, raise some sort of exception
        return False
    
    pass_list = pass_row.past_password.split(", ")
    hashed_pass = hash_pass(new_pass)

    # Check for duplicates
    if hashed_pass in pass_list:
        # Display error message to user and require them to choose new password
        return False
    
    # Update password and list of past passwords
    cursor.execute(f"SELECT * FROM Users WHERE user_id='{user_id}'")
    old_pass = cursor.fetchone().password_hash

    cursor.execute(f"UPDATE Users SET password_hash='{hashed_pass}' WHERE user_id='{user_id}'")

    pass_list.append(old_pass)
    list_str  = ''.join(pass_list)
    cursor.execute(f"UPDATE Passwords SET past_password='{list_str}' WHERE user_id='{user_id}'")

    return True