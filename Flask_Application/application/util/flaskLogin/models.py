from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from application import login_manager
# Base = declarative_base()



# class User(Base):
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = db.Column(String(100), unique=True)
    hashpass = db.Column(String(255))
    fullname = db.Column(String(100))
    role = db.Column(String(255))
    created_on = db.Column(DateTime(timezone=True), server_default=func.now())

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.hashpass, password)


    def set_password(self, password):
        """Create hashed password."""
        self.hashpass = generate_password_hash(password,method='sha256')

# User loader function, keeps track of a user's ID and session, required to keep track of login status
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
