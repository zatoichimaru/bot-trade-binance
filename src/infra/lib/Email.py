# -*- coding: utf-8 -*-
import smtplib, ssl

class Email():

    def __init__( self, smtpServer, port, emailAuth, passAuth ):
        self.smtpServer = smtpServer
        self.port = port
        self.emailAuth = emailAuth
        self.passAuth = passAuth

    def send( self, email, subject, body ):

        try:
            
            message = f"""\
                Subject: {subject}
                To: {email}
                From: {self.emailAuth}
                {body}."""

            context = ssl.create_default_context()

            with smtplib.SMTP( self.smtpServer, self.port ) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login( self.emailAuth, self.passAuth )
                server.sendmail( self.emailAuth, email, message )
        except:
            return None