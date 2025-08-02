from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

domain_systems = Table(
    "domain_systems", Base.metadata,
    Column("domain_id", UUID, ForeignKey("domains.id", ondelete="CASCADE"), primary_key=True),
    Column("system_id", UUID, ForeignKey("systems.id", ondelete="CASCADE"), primary_key=True)
)