
def data_is_valid(data, required):
    if not data:
        return False
    for x in required:    
        if (x not in data) or (not data.get(x)):
            return False
    return True