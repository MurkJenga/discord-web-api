from flask import Blueprint, request
from utils.functions import req_is_valid, parse_request_json
from utils.database_executions import execute_query
from utils.queries import queries

emoji_blueprint = Blueprint('emoji_blueprint', __name__)

@emoji_blueprint.route('/insert', methods=['POST'])
def insert_emoji():
    try:
        data = parse_request_json()
        emoji_args = ['userId', 'messageId', 'emojiName', 'emojiId', 'channelId', 'guildId', 'updateTIme']

        userId = data.get('userId')
        messageId = data.get('messageId')
        emojiName = data.get('emojiName')
        emojiId = data.get('emojiId')
        channelId = data.get('channelId')
        guildId = data.get('guildId')
        updateTIme = data.get('updateTIme')
        request_keys = data.keys()
        
        if req_is_valid(emoji_args, request_keys): 
            execute_query(
                queries['insert_emoji'],
                'insert',
                f'Emoji {emojiName} from {userId} inserted',
                args=(userId, messageId, emojiName, emojiId, channelId, guildId, updateTIme)
            )
            return f'Emoji {emojiName} from {userId} inserted', 200
        else:
            return 'Missing Request Parameters', 400
        
    except Exception as e:
        return str(e), 500 

@emoji_blueprint.route('/delete', methods=['POST'])
def delete_emoji():
    try:
        data = parse_request_json()
        emoji_args = ['updateTIme', 'messageId', 'userId', 'emojiName']
        updateTime = data.get('updateTIme')
        messageId = data.get('messageId')
        userId = data.get('userId')
        emojiName = data.get('emojiName')
        request_keys = data.keys()

        if req_is_valid(emoji_args, request_keys): 
            execute_query(
                queries['delete_emoji'],
                'update',
                f'Emoji {emojiName} from {userId} removed',
                args=(updateTime, messageId, userId, emojiName))
            return f'Emoji {emojiName} from {userId} removed', 200
        else:
            return 'Missing Request Parameters', 400
        
    except Exception as e:
        return str(e), 500      