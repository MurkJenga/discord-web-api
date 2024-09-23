from flask import Flask
from routes.message import message_blueprint
from routes.emoji import emoji_blueprint
from routes.command import command_blueprint
import logging

app = Flask(__name__)
app.register_blueprint(message_blueprint, url_prefix = '/message')
app.register_blueprint(emoji_blueprint, url_prefix = '/emoji')
app.register_blueprint(command_blueprint, url_prefix = '/command')

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
