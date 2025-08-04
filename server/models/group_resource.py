from tokenize import String
from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

group_resources = Table(
    "group_resources", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", String, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
)
