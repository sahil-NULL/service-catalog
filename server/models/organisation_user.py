from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

organisation_users = Table(
    "organisation_users", Base.metadata,
    Column("organisation_id", UUID, ForeignKey("organisations.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)