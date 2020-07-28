"""
jidp2 index (main) view.

URLs include:
/
"""
import flask
import jidp2

from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail, Message

import datetime
from datetime import datetime

from jidp2.IBM import predicIBM
from jidp2.PowerUsage import predicPowerUsage

from jidp2.api.helper import detectingAbnormal


model_path = "jidp2/models/"
data_path = "jidp2/data/"


def read():
    datas = []
    count = -1;
    with open("./first-2000.txt") as f:
        for line in f.readlines():
            count = (count + 1) % 4;

            if (count == 0):
                data = [datetime.strptime(line, '%Y-%m-%d %H:%M:%S\n').replace().timestamp() * 1000]
            elif (count == 1):
                data.append(float(line.split('[')[1].split()[0]))
            elif (count == 3):
                data.append(float(line))
                datas.append(data)
    return datas


# data[i][0] time     '2006-12-20 04:00:00'    最好可以直接是时间戳 1166605200
# data[i][1] actual val
# data[i][2] predic val
def gen(datas, std, threshold):
    all_datas = []
    abnormal_datas = []
    error = std * threshold
    for data in datas:
        all_datas.append([data[0], data[1]])
        if data[1] < data[2] - error or data[1] > data[2] + error:
            abnormal_datas.append([data[0], data[1]])

    return all_datas, abnormal_datas


mail = Mail(jidp2.app)

recipients = []
abnormal_msg = ""


@jidp2.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    dates_IBM, actual_IBM, predicted_stock_price_clstm, predicted_stock_price = predicIBM(model_path=model_path,
                                                                                          data_path=data_path)
    datas_IBM, abnormal_data_IBM, predic_clstm_IBM, predic_traditional_IBM, predic_FCL_IBM = detectingAbnormal(
        dates_IBM, actual_IBM, predicted_stock_price_clstm, predicted_stock_price, [])


    dates_Power, actual_Power, predicted_power_clstm, predicted_power_traditional, predicted_power_FCL = predicPowerUsage(
        model_path=model_path, data_path=data_path)
    datas_Power, abnormal_data_Power, predic_clstm_Power, predic_traditional_Power, predic_FCL_Power = detectingAbnormal(
        dates_Power, actual_Power, predicted_power_clstm, predicted_power_traditional, predicted_power_FCL)
    # data=read();
    # all_data,abnormal_data = gen(data,1,1)
    # predicPowerUsage(model_path=model_path,data_path=data_path)

    style = flask.url_for('static', filename='css/style.css')

    ctx = {'style': style, 'all_data_IBM': datas_IBM, 'abnormal_data_IBM': abnormal_data_IBM,
           'predic_clstm_IBM': predic_clstm_IBM, 'predic_traditional_IBM': predic_traditional_IBM,
           'predic_FCL_IBM': predic_FCL_IBM,
           'all_data_Power': datas_Power, 'abnormal_data_Power': abnormal_data_Power,
           'predic_clstm_Power': predic_clstm_Power, 'predic_traditional_Power': predic_traditional_Power,
           'predic_FCL_Power': predic_FCL_Power

           }


    if recipients:
        msg = mail.send_message(
            '[Anomaly Detected] An anomaly is detected in ' + abnormal_msg,
            sender='jidpalert@gmail.com',
            # In format ['zhuboying@sjtu.edu.cn','hyinghui@umich.edu']
            recipients=recipients,
            body="Dear user\n, An anomaly is detected in" + abnormal_msg
                 + "! To get more information, please visit the main site."
        )
    return flask.render_template("index.html", **ctx)
