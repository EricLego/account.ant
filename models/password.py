import pyodbc;
import jwt;
from passlib.context import CryptContext;
from datetime import datetime, timedelta, timezone;

# Much of this script is based on the one on this page: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

class Token:
    access_token: str
    token_type: str

# Establish DB connection
cnxnStr = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:account-ant.database.windows.net,1433;Database=account-ant-employee;Uid=workerAnt;Pwd=forTheColony01!!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

cnxn = pyodbc.connect(cnxnStr)

cursor = cnxn.cursor()

# Encryption details
SECRET_KEY = "8bb273198502d80891729dc170355c31"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create encryption context
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Functions
def verify_password(plain, hashed):
    return pass_context.verify(plain, hashed)

def hash_pass(plain):
    return pass_context.hash(plain)

def get_user(username: str):
    cursor.execute(f"SELECT * FROM Users WHERE Username='{username}'")
    loginRow = cursor.fetchone()

    # check if retrieval was successful
    if loginRow == None:
        return False
    else:
        return loginRow

def auth_user(username: str, password: str):
    user = get_user(cursor, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, lifetime: timedelta):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + lifetime
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(form_data):
    user = auth_user(form_data.username, form_data.password)
    if not user:
        # Create error message
        print("TO BE IMPLEMENTED")
    else:
        # Create access token
        token_lifetime = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": user.username}, lifetime=token_lifetime
        )
        return Token(access_token=new_access_token, token_type="bearer")