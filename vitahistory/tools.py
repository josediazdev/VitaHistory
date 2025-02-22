from flask import url_for, current_app
from datetime import datetime
import secrets
import os
from PIL import Image
import sendgrid 
from sendgrid.helpers.mail import *

def get_current_year():
    return datetime.now().year


def get_current_time():
    return datetime.now()


def save_picture(user_picture):
    # Genera un nombre único para la imagen usando tokens aleatorios
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(user_picture.filename)
    picture_filename = random_hex + f_ext

    # Construye el ruta completa donde se guardará la imagen
    picture_path = os.path.join(current_app.root_path, 'static/image', picture_filename)

    # Redimensiona la imagen a una resolución de 100x100 pixels
    output_size = (100, 100)
    new_image = Image.open(user_picture)
    new_image.thumbnail(output_size)

    # Guarda la imagen en el directorio especificado
    new_image.save(picture_path)

    # Devuelve el nombre del archivo guardado para su uso posterior
    return picture_filename


    #send_reset_email(user, user.email, user.username)
def send_reset_email(user, to_email, to_username):
    """
    Esta función envía un correo electrónico con un enlace de reseteo de contraseña al usuario.

    Args:
    user (User): El objeto User que contiene la información del usuario.
    to_email (str): La dirección de correo electrónico al que se enviará el correo.
    to_username (str): El nombre de usuario del usuario.
    """

    email = "correo@personalizado.com"

    token = user.get_reset_token()

    message = """
    Para resetear la contraseña, visita el siguiente link: {}. 
    Si no hiciste la solicitud de este mensaje, solo ignoralo y no habrá ningún cambio en tu usuario de VitaHistory
    """.format(url_for('auth.reset_final', token=token, _external=True))

    sg = sendgrid.SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"])

    from_email = Email(email)
    to_email = To(to_email, \
            substitutions={
            "-name-": to_username,
            "-email-": to_email,
            "-message-": message,
        })

    subject = "Información de reseteo de contraseña de VitaHistory"

    html_content = """
        <p>Información de reseteo de clave perteneciente a:</p>
        <p>Nombre de usuario: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """

    mail = Mail(from_email, to_email, subject, html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response)
