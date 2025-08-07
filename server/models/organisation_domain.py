from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

organisation_domains = Table(
    "organisation_domains", Base.metadata,
    Column("organisation_id", String, ForeignKey("organisations.id", ondelete="CASCADE"), primary_key=True),
    Column("domain_id", String, ForeignKey("domains.id", ondelete="CASCADE"), primary_key=True)
)
