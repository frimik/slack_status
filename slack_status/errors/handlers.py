from flask import render_template
from slack_status import app
from slack_status.errors import blueprint as errors


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@errors.app_errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template("500.html"), 500
