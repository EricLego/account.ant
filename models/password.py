import pyodbc
import jwt
from passlib.context import CryptContext
from datetime import date, datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Much of this script is based on the one on this page: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

class Token:
    access_token: str
    refresh_token: str
    token_type: str
    
# Load environment variables from .env file
load_dotenv()

# Establish DB connection
# TODO: swap out local connection code with calls to db_config.py or .env file
DB_USER = "workerAnt"
DB_PASS = "forTheColony01!!"

cnxnStr = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:account-ant.database.windows.net,1433;Database=account-ant-employee;Uid={DB_USER};Pwd={DB_PASS};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

cnxn = pyodbc.connect(cnxnStr)

cursor = cnxn.cursor()

# Encryption details
# TODO: transfer these constants to .env file
SECRET_KEY = "8bb273198502d80891729dc170355c31"
REFRESH_SECRET_KEY = "c473010cc73ad307721ca2736385c61c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 30

# Create encryption context
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Functions
# Returns if a given plaintext password matches a hashed password
def verify_password(plain, hashed):
    return pass_context.verify(plain, hashed)

# Returns the hashed form of a given plaintext password
def hash_pass(plain):
    return pass_context.hash(plain)

# Returns the Users table row corresponding to a given username, or False if not found
def get_user(username: str):
    cursor.execute(f"SELECT * FROM Users WHERE Username='{username}'")
    login_row = cursor.fetchone()

    # check if retrieval was successful
    if login_row == None:
        return False
    else:
        return login_row

# Returns the Users table row corresponding to a given username and plaintext password if valid, or False if either is invalid
def auth_user(username: str, password: str):
    user = get_user(cursor, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

# Returns a token with the given dictionary of claims, secret key, and lifetime
def create_token(data: dict, secret, lifetime: timedelta):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + lifetime
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, secret, algorithm=ALGORITHM)
    return encoded_jwt

# Function that takes in form data from the login screen as a dictionary
# Returns an access and refresh token pair if the data contains a valid login, else returns False
def login(form_data):
    # Authenticate user
    user = auth_user(form_data.username, form_data.password)

    if not user:
        # User doesn't exist, create error message
        return False
    elif user.status == 1:
        # User currently suspended, create error message
        return False
    else:
        # Check for expired password
        cursor.execute(f"SELECT * FROM Passwords WHERE user_id='{user.user_id}'")
        pass_row = cursor.fetchone()
        
        if pass_row == None:
            # Password table doesn't contain user, create error message
            return False
        else:
            # Convert SQL date to Python date
            exp_date = date.fromisoformat(pass_row.expiry_date)
            if exp_date > datetime.now(timezone.utc).date():
                # Password has expired, create error message
                return False
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

# Returns if the provided access token is valid, otherwise returns False
def auth_access_token(token):
    # Check if token is in DB
    cursor.execute(f"SELECT * FROM Access_Tokens WHERE token_hash='{token}'")
    token_row = cursor.fetchone()

    if token_row == None:
        # Token not in database, create error message
        return False
    
    decoded_jwt = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
    if decoded_jwt["exp"] > datetime.now(timezone.utc):
        # Token expired, create error message and maybe attempt refresh using refresh token
        return False
    
    return True

# Returns if the provided refresh token is valid, otherwise returns False
def auth_refresh_token(token):
    # Check if token is in DB
    cursor.execute(f"SELECT * FROM Refresh_Tokens WHERE token_hash='{token}'")
    token_row = cursor.fetchone()

    if token_row == None:
        # Token not in database, create error message
        return False
    
    decoded_jwt = jwt.decode(token, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    if decoded_jwt["exp"] > datetime.now(timezone.utc):
        # Token expired, create error message
        return False
    
    return True

# Returns if the provided plaintext password is an allowed new password for the provided user_id
def update_pass(user_id, new_pass):
    # Retrieve list of past passwords
    cursor.execute(f"SELECT * FROM Passwords WHERE user_id='{user_id}'")
    pass_row = cursor.fetchone()

    if pass_row == None:
        # Given user doesn't exist in the passwords table, raise some sort of exception
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

# Method that takes in the form data for the 'forgot password' screen as a dictionary
# Returns False if given invalid inputs and the security question for the given user if valid
def forgot_pass(form_data):
    # Check if username and email match a user
    user = get_user(form_data.username)

    if not user:
        # User not found, display error message
        return False
    
    if not user.email == form_data.email:
        # Email given is incorrect, display error message
        return False

    cursor.execute(f"SELECT * FROM Security_Questions WHERE user_id='{user.user_id}'")
    question_row = cursor.fetchone()

    if question_row == None:
        # Given user doesn't exist in security question table, raise some sort of exception
        return False

    return question_row.question

# Method that takes in a username and an answer for their security question
# Returns whether or not the answer was correct
def security_question(username, answer):
    # Check if username and email match a user
    user = get_user(username)

    if not user:
        # User not found, display error message
        return False

    cursor.execute(f"SELECT * FROM Security_Questions WHERE user_id='{user.user_id}'")
    question_row = cursor.fetchone()

    if question_row == None:
        # Given user doesn't exist in security question table, raise some sort of exception
        return False

    return question_row.answer == answer