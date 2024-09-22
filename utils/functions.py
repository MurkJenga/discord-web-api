from utils.database_executions import execute_query
from utils.queries import queries
from datetime import datetime
from flask import request

def req_is_valid(check_req_args, req_args): 
    for arg in check_req_args:
        if arg not in req_args:
            return False
    return True

def query_handler(query_key, action, log_message, *args): 
    try: 
        return execute_query(queries[query_key], action, log_message, args=args), 200
    except Exception as e:
        return str(e), 500
    
def return_date(include_time):
    if include_time:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.now().strftime("%Y-%m-%d")
    
def parse_request_json(): 
    try:
        return request.get_json(force=True)
    except Exception as e:
        raise ValueError("Invalid JSON data") from e