class User:
    def __init__(self, _id, username, password):  # we are using _id because id is a python keyword
        self.id = _id
        self.username = username
        self.password = password
