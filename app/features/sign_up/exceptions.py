
class SignUpError(Exception):
    """Clase base para errores de registro de usuario."""
    pass


class UserNameAlreadyExistsError(SignUpError):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"El usuario {username} ya existe")

class EmailAlreadyExistsError(SignUpError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"El correo electrónico {email} ya está en uso")