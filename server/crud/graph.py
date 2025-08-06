from sqlalchemy.orm import Session
from ..models.system_component import SystemComponent
from ..models.component import Component
from ..models.component_dependency import ComponentDependency
from ..models.system import System
from ..models.component_resource import component_resources
from ..models.component_api import ComponentAPI
from ..models.resource import Resource
from ..models.api import API

def get_system_graph_data(db: Session, system_id: str):
    # Step 0: Fetch system
    system = db.query(System).filter_by(id=system_id).first()
    
    # Step 1: Fetch all system-component links (direct + indirect)
    all_links = db.query(SystemComponent).filter_by(system_id=system_id).all()

    if not all_links:
        return {"nodes": [], "edges": []}

    # Step 2: Separate direct links for edge drawing
    direct_links = [link for link in all_links if link.type == "direct"]

    # Step 3: Get all unique component IDs linked to the system
    component_ids = list({link.component_id for link in all_links})

    # Step 4: Fetch all components
    components = db.query(Component).filter(Component.id.in_(component_ids)).all()

    # Step 5: Fetch all component dependencies where source or target is in the system
    dependencies = db.query(ComponentDependency).filter(
        ComponentDependency.source_component_id.in_(component_ids) |
        ComponentDependency.target_component_id.in_(component_ids)
    ).all()

    # Step 6: Build nodes
    nodes = [{"id": str(comp.id), "label": comp.name, "type": "component"} for comp in components]
    nodes.append({
        "id": f"{system_id}",
        "label": f"{system.name}",
        "type": "system"
    })

    # Step 7: Build edges
    edges = []

    # Direct system → component edges
    for link in direct_links:
        edges.append({
            "id": f"{system_id}-{link.component_id}",
            "source": f"system-{system_id}",
            "target": str(link.component_id),
            "type": "direct"
        })

    # Component → component dependency edges
    for dep in dependencies:
        edges.append({
            "id": f"{dep.source_component_id}-{dep.target_component_id}",
            "source": str(dep.source_component_id),
            "target": str(dep.target_component_id),
            "type": "indirect"
        })

    return {"nodes": nodes, "edges": edges}

def get_component_graph_data(db: Session, root_component_id: str):
    visited = set()
    stack = [root_component_id]

    all_dependencies = []
    all_component_ids = set()

    while stack:
        current_id = stack.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        all_component_ids.add(current_id)

        # Fetch outgoing dependencies from current component
        deps = db.query(ComponentDependency).filter(
            ComponentDependency.source_component_id == current_id
        ).all()

        for dep in deps:
            all_dependencies.append(dep)
            if dep.target_component_id not in visited:
                stack.append(dep.target_component_id)

    # ✅ Fetch all component data
    components = db.query(Component).filter(Component.id.in_(all_component_ids)).all()

    # ✅ Fetch resource + API links
    resource_links = db.query(component_resources).filter(
        component_resources.c.component_id.in_(all_component_ids)
    ).all()

    api_links = db.query(ComponentAPI).filter(
        ComponentAPI.component_id.in_(all_component_ids)
    ).all()

    resource_ids = {row.resource_id for row in resource_links}
    api_ids = {row.api_id for row in api_links}

    resources = db.query(Resource).filter(Resource.id.in_(resource_ids)).all()
    apis = db.query(API).filter(API.id.in_(api_ids)).all()

    # ✅ Build nodes
    nodes = [
        {
            "id": str(comp.id),
            "label": comp.name,
            "type": "component",
            "isRoot": comp.id == root_component_id
        }
        for comp in components
    ] + [
        {
            "id": f"{res.id}",
            "label": res.name,
            "type": "resource"
        }
        for res in resources
    ] + [
        {
            "id": f"{api.id}",
            "label": api.name,
            "type": "api"
        }
        for api in apis
    ]

    # ✅ Build edges
    edges = [
        {
            "id": f"{dep.source_component_id}_{dep.target_component_id}",
            "source": str(dep.source_component_id),
            "target": str(dep.target_component_id),
            "type": "dependency"
        }
        for dep in all_dependencies
    ] + [
        {
            "id": f"{link.component_id}_{link.resource_id}",
            "source": str(link.component_id),
            "target": f"resource-{link.resource_id}",
            "type": "uses_resource"
        }
        for link in resource_links
    ] + [
        {
            "id": f"{link.api_id}_{link.component_id}" if link.role == "provides"
            else f"{link.component_id}-api-{link.api_id}",
            "source": f"api-{link.api_id}" if link.role == "provides" else str(link.component_id),
            "target": str(link.component_id) if link.role == "provides" else f"api-{link.api_id}",
            "type": f"{link.role}_api"
        }
        for link in api_links
    ]

    return {"nodes": nodes, "edges": edges}


