from dataclasses import dataclass

from datetime import datetime

@dataclass
class ProjectEntity:
    title: str
    description: str
    status_name: str
    id: int | None = None
    created_at: datetime | None = None
    

@dataclass
class ProjectMemberEntity:
    project_id: int
    user_id: int
    role_id: int
    created_at: datetime | None = None
    id: int | None = None