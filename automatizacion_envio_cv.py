import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuración del servidor SMTP (Gmail en este caso)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "emailejemplo@gmail.com"
GMAIL_PASSWORD = "contraseña"


# Función para enviar correo con adjunto
def enviar_correo(destinatario):
    try:
        # Crea el mensaje del correo
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = destinatario
        msg['Subject'] = "Envío de CV - Solicitud de empleo"

        # Cuerpo del correo
        body = "Hola, te adjunto mi currículum vitae para su consideración. ¡Saludos!"
        msg.attach(MIMEText(body, 'plain'))

        # Ruta del archivo que se va a adjuntar (tu CV)
        archivo_adjunto = r'rutadelCV.pdf'  # Cambia esta ruta por la de tu archivo CV

        # Verificar si el archivo adjunto existe antes de intentar enviarlo
        if not os.path.exists(archivo_adjunto):
            print(f"El archivo {archivo_adjunto} no existe.")
            return False

        # Adjuntar el archivo
        with open(archivo_adjunto, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(archivo_adjunto)}")
            msg.attach(part)

        # Conexión al servidor SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)

        # Envía el correo
        server.send_message(msg)
        print(f"Correo enviado a {destinatario}")
        server.quit()

        return True
    except Exception as e:
        print(f"Error al enviar a {destinatario}: {e}")
        return False


# Lee los correos desde un archivo .txt o .csv
def leer_destinatarios(archivo):
    if not os.path.exists(archivo):
        print(f"El archivo {archivo} no existe en el directorio actual: {os.getcwd()}")
        return []

    with open(archivo, 'r') as file:
        destinatarios = file.read().splitlines()

    if not destinatarios:
        print("La lista de destinatarios está vacía.")

    return destinatarios


# Guarda los emails fallidos en un archivo .txt
def guardar_emails_fallidos(fallidos):
    with open('emails_fallidos.txt', 'w') as file:
        for email in fallidos:
            file.write(email + '\n')
    print("Se guardaron los emails fallidos en emails_fallidos.txt.")


# Función principal para envío masivo de emails
def enviar_emails_masivos():
    archivo_destinatarios = r'ruta_Archivo.txt'  # Cambia esta ruta si es necesario
    lista_destinatarios = leer_destinatarios(archivo_destinatarios)

    if not lista_destinatarios:
        print("No se encontraron destinatarios o el archivo está vacío.")
        return

    emails_fallidos = []

    for email in lista_destinatarios:
        if not enviar_correo(email):
            emails_fallidos.append(email)  # Si falla, se guarda en la lista

    if emails_fallidos:
        guardar_emails_fallidos(emails_fallidos)  # Guardar emails fallidos en archivo
    else:
        print("Todos los correos fueron enviados correctamente.")


# Ejecutar el envío masivo
enviar_emails_masivos()

