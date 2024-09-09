from flask import Blueprint, request
from utils.functions import req_is_valid
from utils.database_executions import execute_query
from utils.queries import queries

message_blueprint = Blueprint('message_blueprint', __name__)

@message_blueprint.route('/insert', methods=['POST'])
def insert_message(): 
    try:
        message_args = ['channelId', 'guildId', 'messageId', 'createdTime', 'content', 'ogContent', 'authorId']
        
        if req_is_valid(message_args, request.args): 
            execute_query(
                queries['insert_query'],
                f'insert',
                f'Message ID {str(request.args["messageId"])} inserted',
                args=(
                    str(request.args['channelId']),
                    str(request.args['guildId']),
                    str(request.args['messageId']),
                    request.args['createdTime'],
                    request.args['content'],
                    request.args['ogContent'],
                    str(request.args['authorId'])
                )
            )
            return 'Message inserted', 200
        else:
            return 'Missing Request Parameters', 400
    
    except Exception as e:
        return e, 500
    
@message_blueprint.route('/update', methods=['POST'])
def update_message(): 
    try:
        message_args = ['updated_time', 'content', 'messageId'] 
        
        if req_is_valid(message_args, request.args):
            msg = {
                'updated_time': request.args['updated_time'],
                'content': request.args['content'],
                'message_id': request.args['messageId'] 
            }
            ## Adding Update Query
            return msg, 200
        
        else:
            return 'Missing Request Parameters', 400
    
    except Exception as e:
        return e, 500
    
@message_blueprint.route('/delete', methods=['POST'])
def delete_message(): 
    try:
        message_args = ['messageId'] 
        
        if req_is_valid(message_args, request.args):
            msg = {
                'message_id': request.args['messageId'] 
            }
            ## Adding Delete Query
            print(f'Message ID {msg["message_id"]} was deleted')
            return msg, 200
        
        else:
            return 'Missing Request Parameters', 400
    
    except Exception as e:
        return e, 500 