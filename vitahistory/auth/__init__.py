from flask import Blueprint, render_template, request, flash, redirect, url_for
from vitahistory import db, bcrypt
from vitahistory.models import User
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from vitahistory.tools import send_reset_email

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('index.start'))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        error1 = None
        error2 = None

        if username:
            user_username = User.query.filter_by(username=username).first()
            if not isinstance(user_username, User):
                error1 = 1
            elif not bcrypt.check_password_hash(user_username.password, password):
                error1 = 1

            user_email = User.query.filter_by(email=username).first()
            if not isinstance(user_email, User):
                error2 = 1
            elif not bcrypt.check_password_hash(user_email.password, password):
                error2 = 1

        if error1 is None or error2 is None:
            login_user(user_username or user_email)

            flash('Haz iniciado sesión exitosamente', 'success')

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('index.start'))

        if error1 is not None and error2 is not None:
            flash("El usuario/correo o contraseña no son válidos, intente nuevamente", 'warning')

    return render_template('auth/login.html')


@auth.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('index.start'))

    if request.method == "POST":
        firstname = request.form["firstname"].title()
        secondname = request.form["secondname"].title()
        email = request.form["email"]
        username = request.form["username"].lower()
        password = request.form["password"]
        password_two = request.form["password_two"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]

        birthdate_time = datetime.strptime(birthdate, "%Y-%m-%d")


        error1 = None
        error2 = None
        error3 = None

        if username:
            user = User.query.filter_by(username=username).first()
            if isinstance(user, User):
                error1 = "El nombre de usuario ya existe, intente con otro por favor"

        if email:
            user = User.query.filter_by(email=email).first()
            if isinstance(user, User):
                error2 = "El correo electrónico ya se encuentra registrado con otro usuario"

        if password != password_two:
            error3 = "Las contraseñas no coinciden, intente nuevamente"

        if error1 is None and error2 is None and error3 is None:
            hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

            user = User(firstname=firstname, secondname=secondname, username=username, \
                    email=email, password=hashed_pass, gender=gender, birthdate=birthdate_time)

            db.session.add(user)
            db.session.commit()

            flash(f'Se ha registrado el usuario {username} exitosamente', 'success')

            return redirect(url_for('auth.login'))

        if error1 is not None:
            flash(error1)
        if error2 is not None:
            flash(error2)
        if error3 is not None:
            flash(error3)


    return render_template('auth/register.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.home'))


@auth.route("reset_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        redirect(url_for('index.start'))


    if request.method == "POST":
        email = request.form["email"]

        error = None

        user_email = User.query.filter_by(email=email).first()

        if not isinstance(user_email, User):
            error = "El usuario no está registrado en la base de datos, intente nuevamente"
        else:
            send_reset_email(user_email, user_email.email, user_email.username)
            flash("Se ha enviado un correo electrónico para resetear la contraseña", "success")

            return redirect(url_for('auth.login'))

        if error is not None:
            flash(error)

    flash('Para resetear la contraseña escribe tu correo electrónico', 'info')

    return render_template('auth/reset_request.html')


@auth.route("reset_final/<token>", methods=["GET", "POST"])
def reset_final(token):
    if current_user.is_authenticated:
        redirect(url_for('index.start'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('El token ingresado no es válido o superó el tiempo de expiración', 'warning')
        return redirect(url_for('auth.reset_request'))

    if request.method == "POST":
        password = request.form["password"]
        password_two = request.form["password_two"]

        error = None

        if password != password_two:
            error = "Las contraseñas no coinciden, intente nuevamente"

        if error is None:
            hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

            user.password = hashed_pass

            flash("La contraseña se ha actualizado correctamente", "success")

            db.session.commit()

            return redirect(url_for('auth.login'))

        if error is not None:
            flash(error)

    flash('Escriba su nueva contraseña', 'info')

    return render_template('auth/reset_final.html')
