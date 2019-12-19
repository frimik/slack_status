"""Top-level package for Slack Status."""

__author__ = """Mikael Fridh"""
__email__ = "mfridh@ea.com"
__version__ = "0.1.0"

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

app = Flask(__name__)
from slack_status.errors import blueprint as errors
from slack_status.emojis import blueprint as emojis

app.register_blueprint(errors)
app.register_blueprint(emojis)

nav.init_app(app)
Bootstrap(app)


@nav.navigation()
def mynavbar():
    return Navbar("Fulhack Industries")


from slack_status import routes
