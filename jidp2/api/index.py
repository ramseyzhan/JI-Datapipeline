"""REST API for index page."""
from flask import session, jsonify, request
from flask_mail import Mail, Message
from os import path, mkdir
import numpy as np
import jidp2
import os
import time 
import datetime 
from jidp2.IBM import predicIBM
from jidp2.PowerUsage import predicPowerUsage
from jidp2.api.helper import format_to_json, detectingAbnormal

threshold = 2;
email =  '';
model_path = "jidp2/models/"
data_path = "jidp2/data/"

jidp2.app.config['MAIL_SERVER']='smtp.gmail.com'
jidp2.app.config['MAIL_PORT'] = 465
jidp2.app.config['MAIL_USERNAME'] = 'jidpalert@gmail.com'
jidp2.app.config['MAIL_PASSWORD'] = 've450dp22'
jidp2.app.config['MAIL_USE_TLS'] = False
jidp2.app.config['MAIL_USE_SSL'] = True



mail = Mail(jidp2.app)

recipients = []
abnormal_msg = ""

@jidp2.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Get all anomalies."""
    to_json = {
        "highchartUrl": "/api/v1/d/",
        "url": "/api/v1/"
    }
    # we need ** in the beginning of the jsonify function
    return jsonify(**to_json)


@jidp2.app.route('/api/v1/', methods=["POST"])
def get_parameters():
    data = request.get_json()
    print(data)
    if 'email' in data:
        email = data['email']
    else:
        email = ''

    threshold = float(data['threshold'])

    tmp_dir = 'tmp'
    try:
        mkdir(tmp_dir)
    except OSError:
        pass

    tmp_para = path.join(tmp_dir, 'parameters.txt')
    with open(tmp_para, 'w') as f:
        f.write(email + '\n' + str(threshold))
    f.close()


    context = {
        'email': email,
        'threshold': threshold
    }
    return jsonify(**context), 201

@jidp2.app.route('/api/v1/i/', methods=["POST"])
def get_inputs():
    data = request.get_json()
    print(data)
    if 'email' in data:
        email = data['email']

    threshold = float(data['threshold'])

    if 'email' in data:
        email = data['email']
    else:
        email = ''

    threshold = float(data['threshold'])

    tmp_dir = 'tmp'
    try:
        mkdir(tmp_dir)
    except OSError:
        pass

    tmp_para = path.join(tmp_dir, 'parameters.txt')
    with open(tmp_para, 'w') as f:
        f.write(email + '\n' + str(threshold))
    f.close()

    fname = data_path+'datasets_IBM_userInput.csv'
    with open(fname, 'a+') as f:
        first_line = f.readline()
        off = -250
        f.seek(0, os.SEEK_END)
        f.seek(f.tell()+off, os.SEEK_SET) 
        last_line = f.readlines()[-1].split(',')
        lasttime = datetime.datetime.strptime(last_line[0],"%Y-%m-%d") 
        modified_date = lasttime + datetime.timedelta(days=1);
        last_line[0]=modified_date.strftime("%Y-%m-%d")
        last_line[2] = data['input'];
        f.seek(0, os.SEEK_END)
        f.write(last_line[0])

        for i in range(1,len(last_line)):
            f.write(','+last_line[i])

    context = {}
    return jsonify(**context), 201



@jidp2.app.route('/api/v1/m/', methods=["GET"])
def get_anomaly():
    """Get all the anomalies."""
    connection = jidp2.model.get_db()
    cur = connection.execute(
        "SELECT * FROM anomaly "
        "ORDER BY anomalyid "
    )
    anomalies = cur.fetchall()
    results = []
    to_json = format_to_json(anomalies, results)
    return jsonify(**to_json)


def convert_to_native_type(*arr2ds):
    for arr2d in arr2ds:
        for arr in arr2d:
            for i in range(len(arr)):
                if isinstance(arr[i], np.float64) or isinstance(arr[i], np.float32):
                    arr[i] = arr[i].item()
    return arr2ds



@jidp2.app.route('/api/v1/d/', methods=["POST"])
def get_chart_data():

    data = request.get_json()

    dataset = data['url'].split('/')[-1]
    if dataset== 'Stock':
        file_name = 'datasets_8388_11883_IBM_2006-01-01_to_2018-01-01.csv'
        dates, actual, predicted_clstm, predicted_traditional = predicIBM(model_path=model_path,
                                                                    file_name=file_name,
                                                                    data_path=data_path)
        data_std = 2
        abnormal_msg = "IBM stock price" 
    elif dataset== 'StockInput' or dataset== 'StockInput?':
        file_name = 'datasets_IBM_userInput.csv'
        dates, actual, predicted_clstm, predicted_traditional = predicIBM(model_path=model_path,
                                                                    file_name=file_name,
                                                                    data_path=data_path)
        data_std = 2
        abnormal_msg = "IBM stock price" 

    else:
        dates, actual, predicted_clstm, predicted_traditional, predicted_power_FCL = predicPowerUsage(
                                                    model_path=model_path, data_path=data_path)
        data_std = 0.5
        abnormal_msg = "PowerUsage" 


    datas, abnormal_data, predic_clstm, predic_traditional, predic_FCL = detectingAbnormal(
        dates, actual, predicted_clstm, predicted_traditional, [],std=data_std,threshold=threshold)


    [datas, abnormal_data, predic_clstm, predic_traditional, predic_FCL] = convert_to_native_type(
        datas,abnormal_data,predic_clstm,predic_traditional,predic_FCL,
    )

    to_json = {
        'all_data': datas, 'abnormal_data': abnormal_data,
        'predic_clstm': predic_clstm, 'predic_traditional': predic_traditional,
        'predic_FCL': predic_FCL, 'dataset': dataset,
        'url': '/api/v1/d/'
    }
    
    try:
        with open('tmp/parameters.txt', 'r') as f:
            email=f.readlines()[0].split()

        if email:

            msg = mail.send_message(
                '[Anomaly Detected] An anomaly is detected in ' + abnormal_msg,
                sender='jidpalert@gmail.com',
                # In format ['zhuboying@sjtu.edu.cn','hyinghui@umich.edu']
                recipients=email,
                body="Dear user\n, An anomaly is detected in" + abnormal_msg
                     + "! To get more information, please visit the main site."
            )
    except Exception as e:
        pass

    return jsonify(**to_json)

