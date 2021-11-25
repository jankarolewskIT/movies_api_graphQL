import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
import graphql_jwt
from django.shortcuts import get_object_or_404
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from .models import Movie, Director


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        """Custom field for MovieType

        Args:
            info (request): info about a request

        Returns:
            str: Movie is Old or New
        """
        return "Old movie" if self.year < 2000 else "New movie"


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director


class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
            "title": ["exact", "icontains", "istartswith", ],
            "year": ["exact", ]
        }
        interfaces = (relay.Node, )


class DirectorNode(DjangoObjectType):
    class Meta:
        model = Director
        filter_fields = {
            "name": ["exact", "icontains", "istartswith", ],
            "surname": ["exact", "icontains", "istartswith", ],
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    all_movies = DjangoFilterConnectionField(MovieNode)
    movie = relay.Node.Field(MovieNode)
    all_directors = DjangoFilterConnectionField(DirectorNode)
    director = relay.Node.Field(DirectorNode)


class MovieCreateMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        """Create an obj and save it in DB
        function check if user is authenticated

        Args:
            info (request): info about request
            title (str): Movie Title
            year (int): Year of movie production

        Returns:
            movie: Movie obj
        """
        movie = Movie.objects.create(title=kwargs.get('title'), year=kwargs.get('year'))

        return MovieCreateMutation(movie)


class MovieUpdateMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True) 
        title = graphene.String()
        year = graphene.Int()

    movie = graphene.Field(MovieType)
    
    @classmethod
    @login_required
    def mutate_and_get_payload(cls,info, id, title, year, **kwargs):
        """Update a movie
        function check if user is authenticated
        Args:
            info (request): info about a request
            id (ID): ID of movie, used as a target to get object to update  
            title (str): Movie title    
            year (int)): Year of movie production

        Returns:
            movie: Updated Movie
        """
        movie = Movie.objects.get(pk=from_global_id(id)[1])
        if title:
            movie.title = title
        if year:
            movie.year = year
        movie.save()

        return MovieUpdateMutation(movie)


class MovieDeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    movie = graphene.Field(MovieType)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        """Mutation for deliting a movie from DB
        function check if user is authenticated

        Args:
            info (request): info about request
            id (ID): Movie ID from DB

        Returns:
            movie: Deleted movie
        """
        movie = Movie.objects.get(pk=from_global_id(kwargs.get('id'))[1])
        if movie:
            movie.delete()

        return MovieDeleteMutation(movie=None)


class Mutation:
    """
    App Mutation class for soring mutations of a Movie
    """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_foken = graphql_jwt.Verify.Field()

    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()
