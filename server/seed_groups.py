# seed_groups.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models.organisation import Organisation
from models.group import Group
import uuid

# Create session
db: Session = SessionLocal()

# Generate organisations
org1_id = str(uuid.uuid4())
org2_id = str(uuid.uuid4())

organisations = [
    {"id": org1_id, "name": "Org Alpha", "description": "First test org"},
    {"id": org2_id, "name": "Org Beta", "description": "Second test org"},
]

# Generate top-level groups
group1_id = str(uuid.uuid4())
group2_id = str(uuid.uuid4())

groups = [
    {"id": group1_id, "name": "Engineering", "organisation_id": org1_id, "parent_group_id": None},
    {"id": group2_id, "name": "Operations", "organisation_id": org1_id, "parent_group_id": None},
]

# Nested sub-groups under Engineering
groups += [
    {"id": str(uuid.uuid4()), "name": "Backend Team", "organisation_id": org1_id, "parent_group_id": group1_id},
    {"id": str(uuid.uuid4()), "name": "Frontend Team", "organisation_id": org1_id, "parent_group_id": group1_id},
    {"id": str(uuid.uuid4()), "name": "DevOps", "organisation_id": org1_id, "parent_group_id": group1_id},
]

# Nested sub-groups under Operations
groups += [
    {"id": str(uuid.uuid4()), "name": "IT Support", "organisation_id": org1_id, "parent_group_id": group2_id},
    {"id": str(uuid.uuid4()), "name": "Security", "organisation_id": org1_id, "parent_group_id": group2_id},
]

# Save all data
try:
    db.bulk_insert_mappings(Organisation, organisations)
    db.bulk_insert_mappings(Group, groups)
    db.commit()
    print("✅ Dummy nested groups inserted successfully.")
except Exception as e:
    db.rollback()
    print("❌ Error inserting dummy data:", e)
finally:
    db.close()
