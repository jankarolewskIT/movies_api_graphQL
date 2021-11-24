from inspect import isbuiltin
import graphene
from .movies.schema import Query as AppQuery

class Query(AppQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)