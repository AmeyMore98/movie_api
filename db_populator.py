import json
from handlers import MovieHandler
from db.database import SessionLocal
from schemas import movie_schema

def pouplate_db_from_json():
    """Populates imdb.db file from imdb.json
    """
    print("Reading JSON file...")
    with open('./imdb.json', 'r') as f:
        json_data = json.load(f)

    print("Creating DB Session")
    db = SessionLocal()

    for item in json_data:
        movie = movie_schema.MovieCreate(**item, popularity=item['99popularity'])
        print("Inserting: {}".format(movie.name))
        MovieHandler.create_movie(db, movie=movie)

if __name__ == '__main__':
    pouplate_db_from_json()
