from domain.interfaces import IRefreshtokenRepository

class InMemoryRefreshTokenRepository(IRefreshtokenRepository):
    def __init__(self):
        self.tokens: dict[int, str] = {}
    
    def save(self, user_id: int, token: str):
        self.tokens[user_id] = token

    def get(self, user_id: int):
        return self.tokens.get(user_id)

    def delete(self, user_id: int):
        if user_id in self.tokens:
            del self.tokens[user_id]