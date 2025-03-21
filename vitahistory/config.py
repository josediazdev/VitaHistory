import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('MYSQL_HOST'),
        os.environ.get('MYSQL_DATABASE')
        )

