# crud/group_api.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.group_api import group_apis
from ..schemas.group_api import GroupApiCreate, GroupApiOut
from ..models.group import Group
from typing import List
from collections import deque
from sqlalchemy import select, insert, delete


def get_all_descendant_group_ids(db: Session, root_group_id: str) -> List[str]:
    """
    Perform BFS to collect all subgroup IDs recursively.
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


def create_group_api(db: Session, link: GroupApiCreate):
    """
    Link API to the group and all its ancestor and descendant groups.
    """
    root_group_id = str(link.group_id)

    # Get full hierarchy of group IDs (ancestors + self + descendants)
    all_group_ids = (
        set(get_all_descendant_group_ids(db, root_group_id)) |
        set(get_all_ancestor_group_ids(db, root_group_id))
    )

    # Step 2: Get existing links to prevent duplication
    existing = db.execute(
        select(group_apis.c.group_id, group_apis.c.api_id).where(
            group_apis.c.api_id == str(link.api_id),
            group_apis.c.group_id.in_(all_group_ids)
        )
    ).fetchall()
    existing_links = {(row.group_id, row.api_id) for row in existing}

    # Step 3: Prepare new unique links
    new_links = [
        {"group_id": gid, "api_id": str(link.api_id)}
        for gid in all_group_ids
        if (gid, str(link.api_id)) not in existing_links
    ]

    if not new_links:
        raise HTTPException(status_code=400, detail="Link(s) already exist")

    # Step 4: Batch insert new links
    db.execute(insert(group_apis), new_links)
    db.commit()
    return GroupApiOut(group_id=link.group_id, api_id=link.api_id)


def get_apis_by_group(db: Session, group_id: str):
    rows = db.execute(
        group_apis.select().where(group_apis.c.group_id == group_id)
    ).fetchall()

    return [GroupApiOut(group_id=row.group_id, api_id=row.api_id) for row in rows]


def delete_group_api(db: Session, link: GroupApiCreate):
    """
    Delete all group-api links for the given group and its descendants.
    """
    # Step 1: Find all relevant group_ids
    all_group_ids = get_all_descendant_group_ids(db, str(link.group_id))

    # Step 2: Perform batch delete
    result = db.execute(
        delete(group_apis).where(
            group_apis.c.group_id.in_(all_group_ids),
            group_apis.c.api_id == str(link.api_id)
        )
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="No matching links found to delete")

    return {"deleted_count": result.rowcount}
