from flask import Blueprint, request
from utils.functions import req_is_valid
from utils.database_executions import execute_query
from utils.queries import queries

command_blueprint = Blueprint('command_blueprint', __name__)

@command_blueprint.route('/given/<emoji>', methods=['GET'])
def given(emoji):
    try:
        result = execute_query(queries["given_query"], 'select', 'Given command used', args=(emoji,)) 
        return result, 200
    
    except Exception as e:
        return str(e), 500 