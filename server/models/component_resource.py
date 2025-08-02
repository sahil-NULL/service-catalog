from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

component_resources = Table(
    "component_resources", Base.metadata,
    Column("component_id", UUID, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", UUID, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
)