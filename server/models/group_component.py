from tokenize import String
from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

group_components = Table(
    "group_components", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("component_id", String, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
)
