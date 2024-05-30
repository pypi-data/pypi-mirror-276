from enum import Enum

class AuthenticationTypes(str, Enum):
    """Enumerator of the Authentication providers."""
    KEY = "key"
    TOKEN = "token"
