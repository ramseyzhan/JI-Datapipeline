"""REST API for index page."""
from flask import session, jsonify, request
from flask_mail import Mail, Message
from os import path, mkdir
import jidp2
from jidp2.IBM import predicIBM
from jidp2.PowerUsage import predicPowerUsage
from jidp2.api.helper import format_to_json, detectingAbnormal


@jidp2.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Get all anomalies."""
    to_json = {
        "highchart": "/api/v1/d/",
        "url": "/api/v1/"
    }
    # we need ** in the beginning of the jsonify function
    return jsonify(**to_json)


@jidp2.app.route('/api/v1/', methods=["POST"])
def get_parameters():
    data = request.get_json()
    email = data['text']
    threshold = data['number']
    tmp_dir = 'tmp'
    mkdir(tmp_dir)
    tmp_para = path.join(tmp_dir, 'parameters.txt')
    with open(tmp_para, 'w+') as f:
        f.write(email + '\n' + threshold)
    f.close()
    context = {
        'email': email,
        'threshold': threshold
    }
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


model_path = "jidp2/models/"
data_path = "jidp2/data/"

mail = Mail(jidp2.app)
recipients = []
abnormal_msg = ""


@jidp2.app.route('/api/v1/d/', methods=["GET"])
def get_chart_data():
    dates_IBM, actual_IBM, predicted_stock_price_clstm, predicted_stock_price = predicIBM(model_path=model_path,
                                                                                          data_path=data_path)
    datas_IBM, abnormal_data_IBM, predic_clstm_IBM, predic_traditional_IBM, predic_FCL_IBM = detectingAbnormal(
        dates_IBM, actual_IBM, predicted_stock_price_clstm, predicted_stock_price, [])

    dates_Power, actual_Power, predicted_power_clstm, predicted_power_traditional, predicted_power_FCL = predicPowerUsage(
        model_path=model_path, data_path=data_path)
    datas_Power, abnormal_data_Power, predic_clstm_Power, predic_traditional_Power, predic_FCL_Power = detectingAbnormal(
        dates_Power, actual_Power, predicted_power_clstm, predicted_power_traditional, predicted_power_FCL)

    datas_IBM = str(datas_IBM)
    abnormal_data_IBM = str(abnormal_data_IBM)
    predic_clstm_IBM = str(predic_clstm_IBM)
    predic_traditional_IBM = str(predic_traditional_IBM)
    predic_FCL_IBM = str(predic_FCL_IBM)
    datas_Power = str(datas_Power)
    abnormal_data_Power = str(abnormal_data_Power)
    predic_clstm_Power = str(predic_clstm_Power)
    predic_traditional_Power = str(predic_traditional_Power)
    predic_FCL_Power = str(predic_FCL_Power)
    to_json = {
        'all_data_IBM': datas_IBM, 'abnormal_data_IBM': abnormal_data_IBM,
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
    return jsonify(**to_json)
