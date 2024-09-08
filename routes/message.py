from flask import Blueprint

message_blueprint = Blueprint('message_blueprint', __name__)

@message_blueprint.route('/total/<date>')
def hello(date):

    return 'hello'
