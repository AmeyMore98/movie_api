from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_read_all_users():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_response = client.post('/login', data=login_payload)
    token = login_response.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = client.get('/users', headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_read_specific_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_response = client.post('/login', data=login_payload)
    token = login_response.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = client.get('/users/user2@gmail.com', headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data['username'] == 'user2@gmail.com'

def test_create_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_user_payload = {
        "username": "testuser@gmail.com",
        "password": "test",
        "is_admin": False
    }
    response = client.post('/users', json=new_user_payload, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 201
    assert response_data['username'] == new_user_payload['username']
    assert response_data['is_admin'] == new_user_payload['is_admin']

def test_create_duplicate_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_user_payload = {
        "username": "testuser@gmail.com",
        "password": "test",
        "is_admin": False
    }
    response = client.post('/users', json=new_user_payload, headers=headers)
    
    assert response.status_code == 400

def test_update_non_existant_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_user_payload = {
        "username": "testuser@gmail.com",
        "password": "test2",
        "is_admin": True
    }
    response = client.put('/users/testuser@gmail.com', json=new_user_payload, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['username'] == new_user_payload['username']
    assert response_data['is_admin'] == new_user_payload['is_admin']

def test_update_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    new_user_payload = {
        "username": "testuser@gmail.com",
        "password": "test2",
        "is_admin": True
    }
    response = client.put('/users/test_user@gmail.com', json=new_user_payload, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 404
    assert response_data['detail'] == "Resource not found"

def test_delete_user():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    login_reponse = client.post('/login', data=login_payload)
    token = login_reponse.json()['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = client.delete('/users/testuser@gmail.com', headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['detail'] == "Resource deleted"
