
-- SYSTEMS
CREATE TABLE systems (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- COMPONENTS
CREATE TABLE components (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- e.g., service, library, website
    owner TEXT,          -- Team or person
    lifecycle TEXT,      -- e.g., production, deprecated
    description TEXT
);

-- SYSTEM_COMPONENTS (Many-to-Many)
CREATE TABLE system_components (
    system_id UUID REFERENCES systems(id) ON DELETE CASCADE,
    component_id UUID REFERENCES components(id) ON DELETE CASCADE,
    PRIMARY KEY (system_id, component_id)
);

-- COMPONENT_DEPENDENCIES (Directed Graph)
CREATE TABLE component_dependencies (
    source_component_id UUID REFERENCES components(id) ON DELETE CASCADE,
    target_component_id UUID REFERENCES components(id) ON DELETE CASCADE,
    description TEXT,
    PRIMARY KEY (source_component_id, target_component_id)
);

-- APIS
CREATE TABLE apis (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,               -- e.g., REST, GraphQL, gRPC
    version TEXT,
    description TEXT
);

-- COMPONENT_APIS (Many-to-Many with role)
CREATE TABLE component_apis (
    component_id UUID REFERENCES components(id) ON DELETE CASCADE,
    api_id UUID REFERENCES apis(id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('provides', 'consumes')),
    PRIMARY KEY (component_id, api_id, role)
);

-- RESOURCES
CREATE TABLE resources (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,               -- e.g., database, s3-bucket
    description TEXT
);

-- COMPONENT_RESOURCES (Many-to-Many)
CREATE TABLE component_resources (
    component_id UUID REFERENCES components(id) ON DELETE CASCADE,
    resource_id UUID REFERENCES resources(id) ON DELETE CASCADE,
    PRIMARY KEY (component_id, resource_id)
);
