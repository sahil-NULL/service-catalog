from sqlalchemy import Table, Column, ForeignKey, String
from ..database import Base

group_users = Table(
    "group_users", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)