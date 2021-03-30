# imports for Simple Mail Transfer Protocol Library
import smtplib
import ssl


class emailService:

    def __init__(self):
        self.sender_email = "YOUR BOT EMAIL HERE" 
        self.receiver_email = "YOUR RECEIVING EMAIL HERE"
        self.port=465
        self.password = "BOT EMAIL PASSWORD HERE"

        # Create a secure SSL Context as per python security considerations -> https://docs.python.org/3/library/ssl.html#ssl-security
        self.cntxt = ssl.create_default_context()

    def send_email(self,message):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.cntxt) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email,
                            self.receiver_email, message)

    def send_email_test(self,message):
        with smtplib.SMTP('localhost', 1025) as server:
            server.sendmail(self.sender_email,
                            self.receiver_email, message)
            print("Successfully sent email")
