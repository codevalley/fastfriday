from fastapi import FastAPI
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from configs.Environment import get_environment_variables
from configs.GraphQL import get_graphql_context
from configs.database import init
from metadata.Tags import Tags
from routers.v1.EventRouter import router as EventRouter
from routers.v1.EventTypeRouter import (
    router as EventTypeRouter,
)
from schemas.graphql.Query import Query
from schemas.graphql.mutations import Mutation

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(EventRouter)
app.include_router(EventTypeRouter)

# GraphQL Schema and Application Instance
schema = Schema(query=Query, mutation=Mutation)
graphql = GraphQLRouter(
    schema,
    graphiql=env.DEBUG_MODE,
    context_getter=get_graphql_context,
)

# Integrate GraphQL Application to the Core one
app.include_router(
    graphql,
    prefix="/graphql",
    include_in_schema=False,
)

# Initialise Data Model Attributes
init()
