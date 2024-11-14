import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_user(client):
    response = client.post('/users', json={'name': 'John Doe', 'email': 'john@example.com'})
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'

def test_get_users(client):
    client.post('/users', json={'name': 'Jane Doe', 'email': 'jane@example.com'})

    response = client.get('/users')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['name'] == 'Jane Doe'
    assert data[0]['email'] == 'jane@example.com'
