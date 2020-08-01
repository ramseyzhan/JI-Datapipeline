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
import jidp2.views.subPage

from jidp2.api.helper import detectingAbnormal


model_path = "jidp2/models/"
data_path = "jidp2/data/"


mail = Mail(jidp2.app)

recipients = []
abnormal_msg = ""


@jidp2.app.route('/', methods=['GET', 'POST'])
def show_index():

    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style}
    return flask.render_template("index.html", **ctx)
