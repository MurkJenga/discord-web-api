from flask import Blueprint, request
from utils.functions import query_handler, return_date
#from utils.queries import queries

command_blueprint = Blueprint('command_blueprint', __name__)

@command_blueprint.route('/given/<emoji>', methods=['GET'])
def given(emoji):
    return query_handler("given_query", 'select', 'Given command used', emoji)

@command_blueprint.route('/recieved/<emoji>', methods=['GET'])
def recieved(emoji):
    return query_handler("recieved_query", 'select', 'Recieved command used', emoji)

@command_blueprint.route('/whogave/<userid>/<emoji>', methods=['GET'])
def whogave(userid, emoji):
    return query_handler("whogave_query", 'select', 'Whogave command used', emoji, userid)

@command_blueprint.route('/whorecieved/<userid>/<emoji>', methods=['GET'])
def whorecieved(userid, emoji):
    return query_handler("whorecieved_query", 'select', 'Whorecieved command used', emoji, userid)

@command_blueprint.route('/total/<date>', methods=['GET'])
def total(date):
    return query_handler("total_query", 'select', 'Total command used', date) 

@command_blueprint.route('/botrequest', methods=['POST'])
def botrequest():
    request_type = request.get_json(force=True)["type"]
    request_text = request.get_json(force=True)["request_text"] 
    return query_handler("botrequest_query", 'insert', 'Botrequest command used', request_type, request_text, return_date(True))

@command_blueprint.route('user/last30/<userid>', methods=['GET'])
def last30(userid):
    return query_handler("last30_query", 'select', 'Last30 command used', userid) 

@command_blueprint.route('/user/<userid>', methods=['GET'])
def user(userid):
    return query_handler("user_query", 'select', 'User command used', userid)