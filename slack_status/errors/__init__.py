from flask import Blueprint

blueprint = Blueprint("errors", __name__)

from slack_status.errors import handlers
