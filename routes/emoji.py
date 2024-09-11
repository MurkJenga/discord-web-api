from flask import Blueprint, request
from utils.functions import req_is_valid
from utils.database_executions import execute_query
from utils.queries import queries

emoji_blueprint = Blueprint('emoji_blueprint', __name__)

@emoji_blueprint.route('/insert', methods=['POST'])
def insert_emoji():
    try:
        emoji_args = ['userId', 'messageId', 'emojiName', 'emojiId', 'channelId', 'guildId', 'updateTIme']
        
        if req_is_valid(emoji_args, request.args): 
            execute_query(
                queries['insert_emoji'],
                'insert',
                f'Emoji {str(request.args["emojiName"])} from {request.args["userId"]} inserted',
                args=(
                    request.args['userId'],
                    request.args['messageId'],
                    request.args['emojiName'],
                    request.args['emojiId'],
                    request.args['channelId'],
                    request.args['guildId'],
                    request.args['updateTIme']
                )
            )
            return f'Emoji {str(request.args["emojiName"])} from {request.args["userId"]} inserted', 200
        else:
            return 'Missing Request Parameters', 400
        
    except Exception as e:
        return str(e), 500 

@emoji_blueprint.route('/delete', methods=['POST'])
def delete_emoji():
    try:
        emoji_args = ['updateTIme', 'messageId', 'userId', 'emojiName']
        
        if req_is_valid(emoji_args, request.args): 
            execute_query(
                queries['delete_emoji'],
                'update',
                f'Emoji {str(request.args["emojiName"])} from {request.args["userId"]} removed',
                args=(
                    request.args['updateTIme'],
                    request.args['messageId'],
                    request.args['userId'],
                    request.args['emojiName']
                )
            )
            return f'Emoji {str(request.args["emojiName"])} from {request.args["userId"]} removed', 200
        else:
            return 'Missing Request Parameters', 400
        
    except Exception as e:
        return str(e), 500      