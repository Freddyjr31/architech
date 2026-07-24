class AuthError(Exception):
    """Base exception for auth module."""
    pass

class UserNotFoundError(AuthError):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Usuario {username} no encontrado")
        
class InvalidCredentialsError(AuthError):
    def __init__(self):
        super().__init__("Credenciales inválidas. Usuario o contraseña incorrectos.")
        
class ErrorChangingPassword(AuthError):
    def __init__(self):
        super().__init__("Error al cambiar la contraseña.")