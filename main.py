import graphene
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp

from api.graphql import Query, Mutations

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.0.133:3000",
    "http://192.168.0.114:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(mutation=Mutations, query=Query)))
app.mount("/static", StaticFiles(directory="static"), name="static")