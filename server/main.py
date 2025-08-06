from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .apis.organisation import router as organisation_router
from .apis.domain import router as domain_router
from .apis.system import router as system_router
from .apis.component import router as component_router
from .apis.resource import router as resource_router
from .apis.api import router as api_router
from .apis.user import router as user_router
from .apis.group import router as group_router
from .apis.component_api import router as component_api_router  
from .apis.component_resource import router as component_resource_router
from .apis.system_component import router as system_component_router
from .apis.domain_system import router as domain_system_router
from .apis.organisation_user import router as organisation_user_router
from .apis.group_user import router as group_user_router
from .apis.group_system import router as group_system_router
from .apis.component_dependency import router as component_dependency_router
from .apis.group_component import router as group_component_router
from .apis.group_resource import router as group_resource_router
from .apis.group_api import router as group_api_router
from .apis.graph import router as graph_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(organisation_router)
app.include_router(domain_router)
app.include_router(system_router)
app.include_router(component_router)
app.include_router(resource_router)
app.include_router(api_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(component_api_router)
app.include_router(component_resource_router)
app.include_router(system_component_router)
app.include_router(domain_system_router)
app.include_router(organisation_user_router)
app.include_router(group_user_router)
app.include_router(group_system_router)
app.include_router(component_dependency_router)
app.include_router(group_component_router)
app.include_router(group_resource_router)
app.include_router(group_api_router)
app.include_router(graph_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}