from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after initializing db
from app.models.account import Account
from app.models.user import User
from app.models.event import Event
from app.models.transaction import Transaction
from app.models.password import Password
from app.models.accesstoken import AccessToken
from app.models.refreshtoken import RefreshToken
