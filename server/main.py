from fastapi import FastAPI
from .database import engine, Base
from . import models
from .apis.organisation import router as organisation_router
from .apis.domain import router as domain_router
from .apis.system import router as system_router
from .apis.component import router as component_router
from .apis.resource import router as resource_router
from .apis.api import router as api_router
from .apis.user import router as user_router

app = FastAPI()

# Include routers
app.include_router(organisation_router)
app.include_router(domain_router)
app.include_router(system_router)
app.include_router(component_router)
app.include_router(resource_router)
app.include_router(api_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}