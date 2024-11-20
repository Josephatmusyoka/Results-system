import os

class Config:
    """Base config class with common settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Secret key for sessions and flash messages
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking to save resources
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///user_data.db'  # Default database URI (SQLite)
    
class DevelopmentConfig(Config):
    """Development configuration class"""
    DEBUG = True  # Enables debugging for development environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_user_data.db'  # Database for development
    
class ProductionConfig(Config):
    """Production configuration class"""
    DEBUG = False  # Disables debugging in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/yourdatabase'  # Example for production database (PostgreSQL)
    
class TestingConfig(Config):
    """Testing configuration class"""
    TESTING = True  # Enables testing mode
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_user_data.db'  # Database for testing
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing purposes
