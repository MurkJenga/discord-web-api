def req_is_valid(check_req_args, req_args): 
    for arg in check_req_args:
        if arg not in req_args:
            return False
    return True