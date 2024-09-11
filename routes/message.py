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
                queries['insert_message'],
                'insert',
                f'Message ID {request.args["messageId"]} inserted',
                args=(
                    request.args['channelId'],
                    request.args['guildId'],
                    request.args['messageId'],
                    request.args['createdTime'],
                    request.args['content'],
                    request.args['ogContent'],
                    request.args['authorId']
                )
            )
            return f'Message {request.args["messageId"]} inserted', 200
        else:
            return 'Missing Request Parameters', 400
        
    except Exception as e:
        return str(e), 500 
        
@message_blueprint.route('/update', methods=['POST'])
def update_message(): 
    try:
        message_args = ['updated_time', 'content', 'messageId'] 
        
        if req_is_valid(message_args, request.args):
            execute_query(
                queries['update_message'],
                'update',
                f'Message ID {request.args["messageId"]} updated',
                args=(
                    request.args['updated_time'],
                    request.args['content'],
                    request.args['messageId']
                )
            ) 
            return f'Message {request.args["messageId"]} Updated', 200
        else:
            return 'Missing Request Parameters', 400

    except Exception as e:
        return str(e), 500 
        
@message_blueprint.route('/delete', methods=['POST'])
def delete_message(): 
    try:
        message_args = ['messageId'] 
        
        if req_is_valid(message_args, request.args): 
            execute_query(
                queries['delete_message'],
                'delete',
                f'Message ID {request.args["messageId"]} deleted',
                args=(
                    request.args['messageId'],
                )
            )
            return 'Message deleted', 200
        
        else:
            return 'Missing Request Parameters', 400
    
    except Exception as e:
        return str(e), 500 