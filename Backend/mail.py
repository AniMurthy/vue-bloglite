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

#used to send email to a fake smtp server and attach a file
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