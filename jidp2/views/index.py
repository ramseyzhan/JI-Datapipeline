"""
jidp2 index (main) view.

URLs include:
/
"""
import flask
import jidp2

from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail,  Message

import datetime
from datetime import datetime



def read():
    datas=[]
    count=-1;
    with open("./first-2000.txt") as f:
        for line in f.readlines():
            count= (count+1) %4;

            if(count==0):
                data = [datetime.strptime(line, '%Y-%m-%d %H:%M:%S\n').replace().timestamp()*1000]
            elif(count==1):
                data.append(float(line.split('[')[1].split()[0]))
            elif(count==3):
                data.append(float(line))
                datas.append(data)
    return datas

# data[i][0] time     '2006-12-20 04:00:00'    最好可以直接是时间戳 1166605200
# data[i][1] actual val
# data[i][2] predic val
def gen(datas,std,threshold):

    all_datas = []
    abnormal_datas = []
    error=std*threshold
    for data in datas:
        all_datas.append([data[0],data[1]])
        if(data[1]<data[2]-error or data[1]>data[2]+error):
            abnormal_datas.append([data[0],data[1]])

    return all_datas,abnormal_datas





jidp2.app.config['MAIL_SERVER']='smtp.gmail.com'
jidp2.app.config['MAIL_PORT'] = 465
jidp2.app.config['MAIL_USERNAME'] = 'jidpalert@gmail.com'
jidp2.app.config['MAIL_PASSWORD'] = 've450dp22'
jidp2.app.config['MAIL_USE_TLS'] = False
jidp2.app.config['MAIL_USE_SSL'] = True

mail = Mail(jidp2.app)

recipients = []
abnormal_msg = ""

@jidp2.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""

    data=read();
    all_data,abnormal_data = gen(data,1,1)


    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style,'all_data':all_data,'abnormal_data':abnormal_data}

    if recipients:
        msg = mail.send_message(
            '[Anomaly Detected] An anomaly is detected in '+abnormal_msg,
            sender='jidpalert@gmail.com',
            # In format ['zhuboying@sjtu.edu.cn','hyinghui@umich.edu']
            recipients=recipients,
            body="Dear user\n, An anomaly is detected in"+abnormal_msg
                +"! To get more information, please visit the main site."
        )
    return flask.render_template("index.html", **ctx)
