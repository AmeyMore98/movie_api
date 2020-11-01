from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from ..db.database import Base
# from imdb_api.routers.dependancies import get_db
from ..main import app

# def override_get_db():
#     SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./tests/test1.db"

#     test_engine = create_engine(
#         SQLALCHEMY_DATABASE_TEST_URL, connect_args={"check_same_thread": False}
#     )
#     TestingSessionLocal = sessionmaker(bind=test_engine)
#     Base.metadata.create_all(bind=test_engine)

#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def test_read__movies_first_100():
    response = client.get('/movies?limit=100')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 100

def test_read_movie():
    response = client.get('/movies/2')
    response_data = response.json()
    expected_data = {
        "name": "Star Wars",
        "director": "George Lucas",
        "popularity": 88.0,
        "imdb_score": 8.8,
        "movie_id": 2,
        "genre": [
            {
                "genre": "Action"
            },
            {
                "genre": "Adventure"
            },
            {
                "genre": "Fantasy"
            },
            {
                "genre": "Sci-Fi"
            }
        ]
    }

    assert response.status_code == 200
    assert response_data == expected_data

def test_read_movie_non_existant():
    response = client.get('/movies/500')
    response_data = response.json()
    expected_data = {
        "detail": "Resource not found"
    }

    assert response.status_code == 404
    assert response_data == expected_data

def test_read_movie_invalid_id():
    response = client.get('/movies/a')
    response_data = response.json()
    expected_data = {
        "detail": [
            {
                "loc": [
                    "path",
                    "movie_id"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }

    assert response.status_code == 422
    assert response_data == expected_data

def test_read_movie_skip_first():
    response = client.get('/movies?skip=1')
    response_data = response.json()
    expected_data = {
        "name": "Star Wars",
        "director": "George Lucas",
        "popularity": 88.0,
        "imdb_score": 8.8,
        "movie_id": 2,
        "genre": [
            {
                "genre": "Action"
            },
            {
                "genre": "Adventure"
            },
            {
                "genre": "Fantasy"
            },
            {
                "genre": "Sci-Fi"
            }
        ]
    }

    assert response.status_code == 200
    assert response_data[0] == expected_data

def test_read_movie_sort_by_name():
    response = client.get('/movies?sort=name')
    response_data = response.json()
    expected_data = {
        "name": "2001 : A Space Odyssey",
        "director": "Stanley Kubrick",
        "popularity": 84.0,
        "imdb_score": 8.4,
        "movie_id": 10,
        "genre": [
            {
                "genre": "Adventure"
            },
            {
                "genre": "Mystery"
            },
            {
                "genre": "Sci-Fi"
            }
        ]
    }

    assert response.status_code == 200
    assert response_data[0] == expected_data


def test_read_movie_sort_by_name_desc():
    response = client.get('/movies?sort=-name')
    response_data = response.json()
    expected_data = {
        "name": "You Only Live Twice",
        "director": "Lewis Gilbert",
        "popularity": 69.0,
        "imdb_score": 6.9,
        "movie_id": 176,
        "genre": [
            {
                "genre": "Action"
            },
            {
                "genre": "Adventure"
            },
            {
                "genre": "Sci-Fi"
            },
            {
                "genre": "Thriller"
            }
        ]
    }

    assert response.status_code == 200
    assert response_data[0] == expected_data

def test_read_movie_filter_imdb_score_lt():
    response = client.get('/movies?imdb_score=lt:7')
    response_data = response.json()
    
    assert response.status_code == 200
    assert max(map(lambda x: x['imdb_score'], response_data)) < 7

def test_read_movie_filter_imdb_score_gt():
    response = client.get('/movies?imdb_score=gt:7')
    response_data = response.json()
    
    assert response.status_code == 200
    assert min(map(lambda x: x['imdb_score'], response_data)) > 7

def test_read_movie_filter_imdb_score_popularity():
    response = client.get('/movies?imdb_score=gte:7&popularity=lt:80')
    response_data = response.json()
    
    assert response.status_code == 200
    assert min(map(lambda x: x['imdb_score'], response_data)) >= 7
    assert min(map(lambda x: x['popularity'], response_data)) < 80

def test_create_movie():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_movie_payload = {
        "name": "The Return of the King",
        "director": "Peter Jackson",
        "popularity": 93.0,
        "imdb_score": 9.3,
        "genre": [
            "Adventure"
        ]
    }
    response = client.post('/movies', json=new_movie_payload, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 201
    assert response_data['name'] == new_movie_payload['name']
    assert response_data['imdb_score'] == new_movie_payload['imdb_score']
    assert response_data['genre'] == [{'genre': 'Adventure'}]

def test_update_movie():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_movie_payload = {
        "name": "The Wizard of Oz",
        "director": "Victor Fleming",
        "popularity": 83.0,
        "imdb_score": 8.3,
        "movie_id": 1,
        "genre": [
            "Musical"
        ]
    }
    response = client.put('/movies/1', json=new_movie_payload, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['name'] == "The Wizard of Oz"
    assert response_data['imdb_score'] == 8.3
    assert response_data['genre'] == [{"genre": "Musical"}]

def test_delete_movie():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = client.delete('/movies/249', headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['message'] == 'Resource deleted'
