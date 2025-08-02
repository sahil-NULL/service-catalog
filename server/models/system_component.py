from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

system_components = Table(
    "system_components", Base.metadata,
    Column("system_id", UUID, ForeignKey("systems.id", ondelete="CASCADE"), primary_key=True),
    Column("component_id", UUID, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
)