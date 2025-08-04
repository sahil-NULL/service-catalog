from tokenize import String
from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from ..database import Base

group_apis = Table(
    "group_apis", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("api_id", String, ForeignKey("apis.id", ondelete="CASCADE"), primary_key=True)
)
