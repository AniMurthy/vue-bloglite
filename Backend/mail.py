from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

# Read these from the config

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "report@bloglite.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message,attachment_file):
    msg = MIMEMultipart ()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText (message,"html"))
    with open(attachment_file,'rb') as file:
        part=MIMEBase("application","octet-stream")
        part.set_payload(file.read())
    encoders.encode_base64(part)
    msg.attach(part)
    s = smtplib.SMTP (host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

# def format message (template_file, data=(}):

# with open (template_file) as file_:

# template = Template (file_. read () )

# return template. render (data=data)

# def send welcome message (data):

# message = format message ("Welcome_email.html", data=data)

# send email (data["email"], subject="Welcome email - 1", message-message)