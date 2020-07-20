"""
jidp2 index (main) view.

URLs include:
/
"""
import flask
import jidp2


@jidp2.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    style = flask.url_for('static', filename='css/style.css')
    ctx = {'style': style}

    return flask.render_template("index.html", **ctx)
