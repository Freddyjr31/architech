from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserEntity:
    id: int
    email: str
    username: str
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    