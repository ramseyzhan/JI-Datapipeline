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



@jidp2.app.route('/Power', methods=['GET', 'POST'])
def show_Power():

    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style}
    return flask.render_template("power.html", **ctx)

@jidp2.app.route('/Stock', methods=['GET', 'POST'])
def show_Stock():

    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style}
    return flask.render_template("stock.html", **ctx)

@jidp2.app.route('/Covid-19', methods=['GET', 'POST'])
def show_Covid():

    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style}
    return flask.render_template("covid.html", **ctx)