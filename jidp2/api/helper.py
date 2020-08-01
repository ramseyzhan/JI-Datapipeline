import flask
import jidp2

from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail, Message

import datetime
from datetime import datetime

from jidp2.IBM import predicIBM
from jidp2.PowerUsage import predicPowerUsage


def format_to_json(anomalies, results):
    to_json = {}
    for anomaly in anomalies:
        anomaly_id = anomaly["anomalyid"]
        results.append({
            "anomalyid": int(anomaly["anomalyid"]),
            "recorded": str(anomaly["recorded"]),
            "global_active_power": float(anomaly["global_active_power"]),
            "global_reactive_power": float(anomaly["global_reactive_power"]),
            "voltage": float(anomaly["voltage"]),
            "global_intensity": float(anomaly["global_intensity"]),
            "sub_metering_1": float(anomaly["sub_metering_1"]),
            "sub_metering_2": float(anomaly["sub_metering_2"]),
            "sub_metering_3": float(anomaly["sub_metering_3"])
        })
    to_json["results"] = results
    to_json["url"] = '/api/v1/m/'
    return to_json


def detectingAbnormal(dates, actual, predicted_clstm, predicted_traditional, predicted_FCL):
    datas = []
    abnormal_data = []
    predic_clstm_data = []
    predic_traditional_data = []
    # predic_FCL should be empty for IBM
    predic_FCL_data = []
    for i in range(len(actual)):
        dateTime = dates[i].timestamp() * 1000
        datas.append([dateTime, actual[i]])
        predic_clstm_data.append([dateTime, predicted_clstm[i]])
        predic_traditional_data.append([dateTime, predicted_traditional[i]])

    for i in range(len(predicted_FCL)):
        dateTime = dates[i].timestamp() * 1000
        predic_FCL_data.append([dateTime, predicted_FCL[i]])

    return [datas, abnormal_data, predic_clstm_data, predic_traditional_data, predic_FCL_data]