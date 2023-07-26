from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from ddc_api.models.user import User
from flask import g
from ddc_api.utils.response import response

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return jsonify(response("failure", "Unauthorized access")), 403
