"""
Designed for notify users via mail
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    """
    Defines an SMTP client session object that can be used to send mail to
    any Internet machine with an SMTP or ESMTP listener daemon.
    """

    def __init__(self, user_name, password, target, server_name='smtp.gmail.com', port=587):
        """Init instance variables

            Attributes:
                user_name (string): sender@gmail.com
                password (string):  password
                target (string): receiver@yahoo.com
                server_name (string): smtp.gmail.com
                port (int): 587

        """
        self.user_name = user_name
        self.password = password
        self.target = target
        self.server_name = server_name
        self.port = port
        self.server = smtplib.SMTP(server_name, port)

    def send_mail(self, subject, message):
        """
        Builds up the mail structure. Connect tot the mail server and send the mail

        Args:
            subject (string): Title of the mail
            message (string): Message in the body of the mail
         """
        msg = MIMEMultipart()
        msg['From'] = self.user_name
        msg['To'] = self.target
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        self.server.connect(self.server_name, self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.user_name, self.password)
        text = msg.as_string()
        self.server.sendmail(self.user_name, self.target, text)


if __name__ == "__main__":
    USER_NAME = 'dummy@gmail.com'
    PASSWORD = 'password'
    TARGET = 'target@gmail.com'
    OBJ = Mail(USER_NAME, PASSWORD, TARGET)
    OBJ.send_mail('HI', 'TEST')
