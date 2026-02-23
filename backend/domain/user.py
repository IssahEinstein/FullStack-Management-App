
class User:
    def __init__(self, username: str, email: str, password_hash: str, id = ""):
        self.id = id # placeholder id to be overridden by automatic id in repository
        self.username = username
        self.email = email
        self.password_hash = password_hash

