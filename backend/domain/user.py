
class User:
    def __init__(self, id: int, username: str, email: str, password_hash: str):
        self.id = 0 # placeholder id to be overridden by automatic id in repository
        self.username = username
        self.email = email
        self.password_hash = password_hash

