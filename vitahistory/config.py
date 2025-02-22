import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lite.db'
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

