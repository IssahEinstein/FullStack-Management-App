class RefreshError(Exception):
    """Base Error for all refresh token errors"""
    pass

class InvalidTokenError(RefreshError):
    """Raises error if token invalid .ie. expires or just plain wrong"""
    pass