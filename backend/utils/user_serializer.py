class UserSerializer:
    @staticmethod
    def to_dict(user):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }