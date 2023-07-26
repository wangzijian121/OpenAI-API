def response(status, msg):
    return {"status": status, "data": msg}


def success(msg):
    return {"status": "success", "data": msg}


def failure(msg):
    return {"status": "failure", "data": msg}
