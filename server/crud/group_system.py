# crud/group_system.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.group_system import group_systems
from ..schemas.group_system import GroupSystemCreate, GroupSystemOut
from ..models.group import Group
from typing import List
from collections import deque
from sqlalchemy import select, insert, delete


def get_all_descendant_group_ids(db: Session, root_group_id: str) -> List[str]:
    """
    Perform BFS to collect all subgroup IDs recursively (downward traversal).
    """
    visited = set()
    queue = deque([root_group_id])

    while queue:
        current_id = queue.popleft()
        if current_id in visited:
            continue
        visited.add(current_id)

        children = db.query(Group.id).filter(Group.parent_group_id == current_id).all()
        queue.extend([str(child.id) for child in children])

    return list(visited)


def get_all_ancestor_group_ids(db: Session, start_group_id: str) -> List[str]:
    """
    Recursively walk up the tree to collect all parent group IDs (upward traversal).
    """
    current_id = start_group_id
    ancestors = set()

    while current_id:
        parent = db.query(Group.parent_group_id).filter(Group.id == current_id).scalar()
        if parent:
            parent_str = str(parent)
            if parent_str not in ancestors:
                ancestors.add(parent_str)
                current_id = parent_str
            else:
                break  # prevent loop
        else:
            break

    return list(ancestors)


def create_group_system(db: Session, link: GroupSystemCreate):
    """
    Link system to the group and all its ancestor and descendant groups.
    """
    root_group_id = str(link.group_id)

    # Get full hierarchy of group IDs (ancestors + self + descendants)
    all_group_ids = (
        set(get_all_descendant_group_ids(db, root_group_id)) |
        set(get_all_ancestor_group_ids(db, root_group_id))
    )

    # Check existing links
    existing = db.execute(
        select(group_systems.c.group_id, group_systems.c.system_id).where(
            group_systems.c.system_id == str(link.system_id),
            group_systems.c.group_id.in_(all_group_ids)
        )
    ).fetchall()
    existing_links = {(row.group_id, row.system_id) for row in existing}

    # Prepare new insertions
    new_links = [
        {"group_id": gid, "system_id": str(link.system_id)}
        for gid in all_group_ids
        if (gid, str(link.system_id)) not in existing_links
    ]

    if not new_links:
        raise HTTPException(status_code=400, detail="Link(s) already exist")

    # Batch insert
    db.execute(insert(group_systems), new_links)
    db.commit()

    return GroupSystemOut(group_id=link.group_id, system_id=link.system_id)


def get_systems_by_group(db: Session, group_id: str):
    rows = db.execute(
        group_systems.select().where(group_systems.c.group_id == group_id)
    ).fetchall()

    system_ids = [row.system_id for row in rows]

    return {
        "group_id": group_id,
        "system_ids": system_ids
    }


def get_groups_by_system(db: Session, system_id: str):
    rows = db.execute(
        group_systems.select().where(group_systems.c.system_id == system_id)
    ).fetchall()

    return [GroupSystemOut(group_id=row.group_id, system_id=row.system_id) for row in rows]


def delete_group_system(db: Session, link: GroupSystemCreate):
    """
    Delete all group-system links for the given group and its descendants.
    """
    # Step 1: Find all relevant group_ids
    all_group_ids = get_all_descendant_group_ids(db, str(link.group_id))

    # Step 2: Perform batch delete
    result = db.execute(
        delete(group_systems).where(
            group_systems.c.group_id.in_(all_group_ids),
            group_systems.c.system_id == str(link.system_id)
        )
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="No matching links found to delete")

    return {"deleted_count": result.rowcount}
