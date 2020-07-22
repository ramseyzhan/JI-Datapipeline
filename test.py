from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail,  Message

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'SJTUPRPSpell@gmail.com'
app.config['MAIL_PASSWORD'] = 'sjtuprpzy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

def send_mail():
    msg = mail.send_message(
        'Send Mail tutorial!',
        sender='SJTUPRPSpell@gmail.com',
        recipients=['zhuboying@sjtu.edu.cn'],
        body="Congratulations you've succeeded!"
    )
    return 'Mail sent'

send_mail()