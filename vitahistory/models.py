from flask import current_app
from vitahistory import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_user = db.Column(db.String(50), nullable=False, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    speciality = db.Column(db.String(80), default='Especialidad')

    persons = db.relationship('Person', backref='author', lazy=True)

    category = db.relationship('Category', backref='cat', lazy=True)

    def get_reset_token(self):
        # Genera un token para verificar la solicitud de cambio de contraseña.
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        """
        Verifica si el token proporcionado es válido.

        Args:
            token (str): El token a verificar.

        Returns:
            User or None: El usuario correspondiente al token si es válido, o None si no es válido.
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try: 
            user_id = s.loads(token, max_age=300)["user_id"]
        except:
            return None

        return User.query.get(user_id)
        

    def __repr__(self):
        return f"User('{self.firstname}','{self.username}', '{self.email}')"


class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(100))
    image_person = db.Column(db.String(50), nullable=False, default='default2.jpg')
    date_in = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    histories = db.relationship('History', backref='patient', lazy=True)

    def __repr__(self):
        return f"Person('{self.fullname}', '{self.email}', '{self.phonenumber}')"


class History(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_out = db.Column(db.DateTime, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    def __repr__(self):
        return f"History('{self.title}', '{self.content}', '{self.date_out}')"


class Category(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Sin categoría')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Category('{self.name}', '{self.user_id}')"

