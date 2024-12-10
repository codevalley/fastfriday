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
- [ ] `pyproject.toml` (if exists): Update project metadata

### Documentation
- [x] `README.md`: 
  - [x] Update title, description, and badges
  - [x] Replace all instances of "fastapi-clean-example"
  - [x] Update installation instructions with Friday-specific details
  - [x] Add sections about life logging features
  - [x] Update API documentation examples to reflect life logging endpoints

- [ ] `docs/*.md`:
  - [ ] Update examples in `api-layer.md` to use life logging contexts
  - [ ] Update domain examples in `domain-models.md` to reflect life events
  - [ ] Update service examples in `application-services.md` with life logging use cases
  - [ ] Review and update all generic examples in architecture documentation

### Code Files
- [ ] Database table names in models (if using generic names)
  - [ ] Rename `books` to `life_events`
  - [ ] Rename `authors` to `event_categories`
  - [ ] Update association table name
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
3. In Progress: Implement changes systematically, starting with core documentation
4. [ ] Update tests to reflect new branding and domain context
5. [ ] Review and update API documentation with new examples

## Domain Model Changes
- [ ] Define core entities:
  - [ ] LifeEvent (replaces Book)
    - id: Integer
    - title: String
    - description: String
    - timestamp: DateTime
    - location: Optional[String]
    - mood: Optional[String]
    - category_id: ForeignKey
  - [ ] EventCategory (replaces Author)
    - id: Integer
    - name: String
    - description: String
    - color: Optional[String]
  - [ ] EventTag
    - id: Integer
    - name: String
  - [ ] EventTagAssociation
    - event_id: ForeignKey
    - tag_id: ForeignKey