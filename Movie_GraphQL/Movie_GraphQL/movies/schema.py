from django.db import models
import graphene
from graphene_django.types import DjangoObjectType
from django.shortcuts import get_object_or_404

from .models import Movie, Director

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New movie"

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())
    all_directors = graphene.List(DirectorType)

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        if id:
            return Movie.objects.get(pk=id)

        if title:
            return Movie.objects.get(title=title) 

        return None
    
    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()

class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)       

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year, **kwargs):
        movie = Movie.objects.create(title=title, year=year)

        return MovieCreateMutation(movie)

class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id =graphene.ID(required=True)

    
    movie = graphene.Field(MovieType)

    def mutate(self, info, id, title, year, **kwargs):
        movie = Movie.objects.get(pk=id)
        if title:
            movie.title = title
        if year:
            movie.year = year
        movie.save()

        return MovieUpdateMutation(movie)

class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = get_object_or_404(Movie, id=id)
        if movie:
            movie.delete()

        return MovieDeleteMutation(movie)

class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()

