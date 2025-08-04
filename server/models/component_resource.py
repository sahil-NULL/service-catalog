from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

component_resources = Table(
    "component_resources", Base.metadata,
    Column("component_id", String, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", String, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
)