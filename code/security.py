import hmac

from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'asdf')
]

# key value pairs
username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)  # added benefit of using get as opposed to using [''], we can use None
    if user and hmac.compare_digest(user.password, password):  # safe string comparison
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
