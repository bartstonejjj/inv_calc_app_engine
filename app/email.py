from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail

import traceback
import smtplib


def send_async_email(app, msg):
    with app.app_context():
        try:
            # Enable SMTP-level debug output
            smtplib.SMTP.debuglevel = 1
            print("📨 Attempting to send email...")
            mail.send(msg)
            print("✅ Email send completed successfully.")
        except Exception as e:
            print("❌ Email send failed!")
            traceback.print_exc()


def send_email(subject, sender, recipients, text_body, html_body):
    print('Sending to', recipients)
    print('Sender', sender)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Investment Calculator] Reset Your Password',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.get_email()],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))