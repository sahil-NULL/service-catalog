from tokenize import String
from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

group_systems = Table(
    "group_systems", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("system_id", String, ForeignKey("systems.id", ondelete="CASCADE"), primary_key=True)
)
