from flask import Blueprint, request, jsonify
from utils.functions import req_is_valid, parse_request_json
from utils.database_executions import execute_query
from utils.queries import queries

message_blueprint = Blueprint('message_blueprint', __name__)

@message_blueprint.route('/insert', methods=['POST'])
def insert_message():
    try:
        data = parse_request_json()
        
        message_args = ['channelId', 'guildId', 'messageId', 'createdTime', 'content', 'ogContent', 'authorId']
        channelId = data.get("channelId")
        guildId = data.get("guildId")
        messageId = data.get("messageId")
        createdTime = data.get("createdTime")
        content = data.get("content")
        ogContent = data.get("ogContent")
        authorId = data.get("authorId")
 
        request_keys = list(data.keys())
        if not req_is_valid(message_args, request_keys):
            return jsonify({"error": "Missing Request Parameters"}), 400

        try:
            execute_query(
                queries['insert_message'],
                'insert',
                f'Message ID {messageId} inserted', 
                args=(channelId, guildId, messageId, createdTime, content, ogContent, authorId))
            return jsonify({"message": f'Message {messageId} inserted'}), 200
        
        except Exception as e: 
            print(f"Database error: {e}")
            return jsonify({"error": "Database error"}), 500
        
    except ValueError as ve: 
        print(f"Invalid JSON error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e: 
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error occurred"}), 500
        
@message_blueprint.route('/update', methods=['POST'])
def update_message(): 
    try:
        data = parse_request_json() 
        message_args = ['updated_time', 'content', 'messageId'] 

        updated_time = data.get('updated_time')
        content = data.get('content')
        messageId = data.get('messageId')
        request_keys = list(data.keys())
        
        if req_is_valid(message_args, request_keys):
            execute_query(
                queries['update_message'],
                'update',
                f'Message ID {messageId} updated',
                args=(updated_time, content, messageId))
             
            return f'Message {messageId} Updated', 200
        else:
            return 'Missing Request Parameters', 400

    except Exception as e:
        return str(e), 500 
        
@message_blueprint.route('/delete', methods=['POST'])
def delete_message(): 
    try: 
        data = parse_request_json() 
        message_args = ['messageId']
        messageId = data.get('messageId')
        request_keys = list(data.keys())
        
        if req_is_valid(message_args, request_keys): 
            execute_query(
                queries['delete_message'],
                'delete',
                f'Message ID {messageId} deleted',
                args=(messageId,))
            return 'Message deleted', 200
        
        else:
            return 'Missing Request Parameters', 400
    
    except Exception as e:
        return str(e), 500 