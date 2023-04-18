from app import schemas
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Test create_user endpoint
def test_create_and_get_user():
    # Create a user to send in the POST request
    user = schemas.UserCreate(name="testuser", email="testuser@example.com", password="testpassword")

    # Send a POST request to the create_user endpoint
    response = client.post("/users/", json=user.dict())

    # Check that the response status code is 201 Created
    assert response.status_code == 201

    user_out = schemas.UserOut(**response.json())
    print(user_out)
    # Check that the returned user has the correct username and email
    assert user_out.email == user.email

    # Check that the returned user has a valid ID
    assert isinstance(user_out.id, int)

    # Send a GET request to the get_user endpoint with the user's ID
    response = client.get(f"/users/{user_out.id}")

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is a UserOut object
    user_out = schemas.UserOut(**response.json())
    assert isinstance(user_out, schemas.UserOut)

    # Check that the returned user has the correct ID, username, and email
    assert user_out.email == user.email