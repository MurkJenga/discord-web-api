from flask import Flask
from routes.message import message_blueprint
import logging

app = Flask(__name__)
app.register_blueprint(message_blueprint, url_prefix = '/message')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run()