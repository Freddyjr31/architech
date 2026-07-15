class ProjectError(Exception):
    """Base exception for Project module."""


class ProjectNotFoundError(ProjectError):
    def __init__(self):
        super().__init__(f"Projecto no encontrado.")


class ProjectNameTakenError(ProjectError):
    def __init__(self, title: str):
        self.title = title
        super().__init__("Ya existe un Projecto con ese nombre.")


class StatusNotFoundError(ProjectError):
    def __init__(self):
        super().__init__("Error de configuración interna.")


class MemberAlreadyAssignedError(ProjectError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__("El usuario ya está asignado a este Projecto.")
        

class NotPermissionToDelete(ProjectError):
    def __init__(self):
        super().__init__("No tienes permiso para eliminar este Projecto.")
