from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

movie_genre_association = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey("movies.movie_id")),
    Column('genre', String, ForeignKey("genres.genre"))
)

class Movie(models.Model):
    movie_id = fields.IntField(pk=True)
    name = fields.CharField(null=False)
    director = fields.CharField(null=False)
    popularity = fields.CharField(null=False)
    imdb_score = fields.CharField(null=False)
    genre: fields.ManyToManyRelation["Genre"] = fields.ManyToManyField(
        "models.movie_model.Movie", related_name='genres', through='movie_genre'
    )

class Genre(Base):
    __tablename__ = 'genres'

    genre = fields.CharField(pk=True)
