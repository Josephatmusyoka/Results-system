from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import db from __init__.py
from sqlalchemy import UniqueConstraint

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)  # Removed unique=True for now
    phone = db.Column(db.String(15), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Define unique constraints with explicit names
    __table_args__ = (
        UniqueConstraint('registration_number', name='uq_registration_number'),
        UniqueConstraint('email', name='uq_email'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
