import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Updated for MySQL
    # Structure: mysql+pymysql://user:password@localhost/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #or \
      #  'mysql+pymysql://root:12345@localhost/finquest'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-key-123'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-key-do-not-use-in-production'
    # Requirement: 12-hour session duration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12) 
    BCRYPT_LOG_ROUNDS = 13

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False  # Add this line explicitly
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')