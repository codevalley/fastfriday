# Branding Changes Required

## Project Overview
Current: Generic FastAPI Clean Architecture Example
Target: Friday - Your Personal Life Logger API

## Files Requiring Changes

### Configuration Files
- [x] `.env`: Update APP_NAME and DATABASE_NAME from "FastAPI Clean Example" and "fastapi_clean_example"
- [x] `Pipfile`: Update project name and description
  - [x] Added metadata section
  - [x] Updated Python version
  - [x] Added convenient scripts
- [x] `pyproject.toml`: Update project metadata
  - [x] Added project section with name and description
  - [x] Added build system configuration
  - [x] Added keywords and license

### Documentation
- [x] `README.md`: 
  - [x] Update title, description, and badges
  - [x] Replace all instances of "fastapi-clean-example"
  - [x] Update installation instructions with Friday-specific details
  - [x] Add sections about life logging features
  - [x] Update API documentation examples to reflect life logging endpoints

- [x] `docs/*.md`:
  - [x] Update examples in `api-layer.md` to use life logging contexts
  - [x] Update domain examples in `domain-models.md` to reflect life events
  - [x] Update service examples in `application-services.md` with life logging use cases
  - [ ] Review and update all generic examples in architecture documentation

### Code Files
- [ ] Database table names in models (if using generic names)
  - [ ] Rename `books` to `life_events`
  - [ ] Rename `authors` to `event_categories`
  - [ ] Update association table name to `event_tag_association`
- [ ] API route prefixes in routers
  - [ ] Update from `/api/v1/books` to `/api/v1/events`
  - [ ] Update from `/api/v1/authors` to `/api/v1/categories`
- [ ] GraphQL schema names and descriptions
  - [ ] Update type names to match new domain
  - [ ] Update field descriptions
  - [ ] Update mutation names
- [ ] Test file naming and test case descriptions
- [ ] Example data in fixtures/seeds

### Docker/Deployment
- [ ] Docker image names and container names
- [ ] Kubernetes manifests (if any)
- [ ] CI/CD pipeline configurations

## Branding Elements to Define
1. Project Name: "Friday" ✓
2. Tagline: "API for Life" ✓
3. Key Features to Highlight: ✓
   - Personal life event logging
   - Daily activity tracking
   - Life data analytics
   - Secure personal data storage

## Database Changes
- [x] Review and rename database from "fastapi_clean_example" to "friday" or "friday_db"
- [ ] Update table names to reflect life logging domain
- [ ] Review column names for clarity in life logging context

## API Changes
- [ ] Update API routes from generic examples to life logging specific endpoints
- [ ] Review and update API documentation to reflect life logging use cases
- [ ] Update GraphQL schema names and descriptions
- [ ] Review error messages and system responses for consistent branding

## Next Steps
1. ✓ Review and prioritize these changes
2. ✓ Create specific tasks for each change
3. ✓ Update core documentation
4. → Update API Layer Implementation (next)
   - [ ] Create/update API routes for events
   - [ ] Update GraphQL schema
   - [ ] Implement event validation
   - [ ] Add filtering and pagination
5. [ ] Update tests to reflect new branding and domain context
6. [ ] Review and update API documentation with new examples

## Domain Model Changes
- [x] Define core entities:
  - [x] LifeEvent
    - id: Integer
    - timestamp: DateTime (indexed)
    - event_type_id: ForeignKey
    - data: JSON
  - [x] EventType
    - id: Integer
    - name: String (unique)
    - description: String
    - schema: JSON (for data validation)
    - icon: String
    - color: String (hex)
    - events: List[LifeEvent]

## Example Event Types (Implemented in seeds/event_types.py)
1. PhotoEvent ✓
2. MealEvent ✓
3. ExerciseEvent ✓
4. NoteEvent 
5. SleepEvent ✓

## Implementation Order
1. ✓ Configuration Files (completed)
2. ✓ Domain Models (completed)
   - [x] Create EventType model
   - [x] Create LifeEvent model
   - [x] Create initial event type seeds
3. → Documentation Updates (next)
4. Database Schema Changes
5. API Layer Updates
6. Testing and Deployment

## Next Steps
1. Update documentation in `docs/` to reflect new domain model
2. Create database migration for the new schema
3. Update API endpoints for life event operations
4. Add JSON Schema validation in the service layer

## Schema Organization

- [x] Move all GraphQL types to `schemas/graphql/types/`
- [x] Move all Pydantic schemas to `schemas/pydantic/`
- [x] Create proper type hierarchy with base classes
- [x] Implement proper field validation
- [x] Fix circular imports between EventType and LifeEvent
- [x] Rename `schema` field to `event_schema` to avoid Pydantic conflicts
- [x] Add proper type stubs for Strawberry GraphQL

## Data Models

- [x] Create SQLAlchemy models for core entities
- [x] Add proper relationships between models
- [x] Add proper indexes and constraints
- [x] Add validation for JSON fields
- [x] Add proper cascade behavior for relationships

## API Layer

- [x] Implement GraphQL mutations
- [x] Implement GraphQL queries
- [x] Add proper error handling
- [x] Add input validation
- [x] Add proper response types
- [x] Add proper documentation

## Service Layer

- [x] Create service classes for business logic
- [x] Add proper error handling
- [x] Add input validation
- [x] Add proper response types
- [x] Add proper documentation

## Recent Progress (2024-01-19)

1. Fixed schema organization:
   - Moved all GraphQL types to dedicated directories
   - Moved all Pydantic schemas to dedicated directories
   - Fixed circular imports by consolidating GraphQL types in models.py
   - Added proper type stubs for Strawberry GraphQL

2. Fixed naming conflicts:
   - Renamed `schema` field to `event_schema` to avoid Pydantic conflicts
   - Updated all references in models, schemas, and services

3. Fixed type system:
   - Added proper type stubs for Strawberry
   - Fixed type hints for JSON fields
   - Added proper null handling for optional fields
   - Fixed forward references and circular dependencies

4. Improved code organization:
   - Added proper package structure
   - Added proper imports
   - Added proper documentation
   - Consolidated related GraphQL types in single file

## Next Steps

1. [ ] Add tests for GraphQL types
2. [ ] Add tests for Pydantic schemas
3. [ ] Add tests for service layer
4. [ ] Add integration tests
5. [ ] Add proper error messages
6. [ ] Add proper logging
7. [ ] Add proper metrics
8. [ ] Add proper monitoring
9. [ ] Add proper deployment configuration
10. [ ] Add proper CI/CD pipeline