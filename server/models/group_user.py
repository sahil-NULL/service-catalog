from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

group_users = Table(
    "group_users", Base.metadata,
    Column("group_id", UUID, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)