from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

organisation_users = Table(
    "organisation_users", Base.metadata,
    Column("organisation_id", String, ForeignKey("organisations.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)