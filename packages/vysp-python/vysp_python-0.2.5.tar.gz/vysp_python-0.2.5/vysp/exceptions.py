class VYSPClientError(Exception):
    """Base class for exceptions in VYSPClient."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class AuthenticationError(VYSPClientError):
    """Raised when there is an authentication issue with the API."""
    pass

class NotFoundError(VYSPClientError):
    """Raised when the requested resource is not found."""
    pass

class BadRequestError(VYSPClientError):
    """Raised when the request is malformed or invalid."""
    pass

class ApiError(VYSPClientError):
    """Raised for general API errors."""
    pass