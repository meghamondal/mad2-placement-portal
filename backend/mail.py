import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_ADDRESS = "support@pportal.in"
SENDER_PASSWORD = ""

def send_email(to, subject, message, content= "html"):
  msg = MIMEMultipart()
  msg['From'] = SENDER_ADDRESS
  msg['To'] = to
  msg['Subject'] = subject

  if content == "html":
    msg.attach(MIMEText(message, "html"))
  else:
    msg.attach(MIMEText(message, "plain"))

  s_client = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT )
  # s_client.login(SENDER_ADDRESS, SENDER_PASSWORD )
  s_client.send_message(msg)
  s_client.quit()

  return True