import datetime
from flask import request, abort, g
from functools import wraps
from models.user import User as UserModel

def get_current_timestamp():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def authenticate_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:  # no header set
            abort(401)
        user = UserModel.query.filter_by(user_name=auth.username).first()
        if user is None or user.password != auth.password:
            abort(401)
        g.user = user
        return f(*args, **kwargs)

    return decorated
