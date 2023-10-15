import smtplib
from email.mime.text import MIMEText



class emailSender:
    sender = "therealchalinosanchez@gmail.com"
    password = "mlta vekc irlj exls"

    def __init__(self,sender,password):
        self.sender = sender
        self.password = password

    def send_email(self, subject, body, recipients, file, code):
        HTMLFile = open(file, "r", encoding="utf-8")
        index = HTMLFile.read()
        index = index.replace("REPLACE-ME",code)
        msg = MIMEText(index, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(self.sender, self.password)
           smtp_server.sendmail(self.sender, recipients, msg.as_string())
        print("Message sent!")


