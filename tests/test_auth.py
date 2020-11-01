from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_login():
    login_payload = {
        'username': 'user1@gmail.com',
        'password': 'user1'
    }
    response = client.post('/login', data=login_payload)
    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data.keys()
    assert 'token_type' in data.keys()
