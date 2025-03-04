from app.extensions import db

# Removed database initialization from here and using extensions to manage it.
from app.models.tokens import Token
from app.models.account import Account
from app.models.user import User
from app.models.event import Event
from app.models.transaction import Transaction
from app.models.password import Password
from app.models.security_questions import SecurityQuestion
