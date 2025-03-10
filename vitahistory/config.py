import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('MYSQL_HOST'),
        os.environ.get('MYSQL_DATABASE')
        )

