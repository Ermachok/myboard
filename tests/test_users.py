import pytest

# Test user data used for registration and login
test_user = {
    "email": "test12@example.com",
    "login": "testuser12",
    "password": "StrongPass123",
}


@pytest.mark.asyncio
async def test_register_user(client):
    # Test user registration endpoint
    response = await client.post("/api/users", json=test_user)
    assert response.status_code == 201  # Expect HTTP 201 Created
    data = response.json()
    # Verify returned user data matches input
    assert data["email"] == test_user["email"]
    assert data["login"] == test_user["login"]
    assert "id" in data  # The response should contain a user ID


@pytest.mark.asyncio
async def test_login_user(client):
    # Ensure user exists by registering before login
    await client.post("/api/users", json=test_user)
    # Test user login endpoint
    response = await client.post(
        "/api/users/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200  # Expect HTTP 200 OK
    data = response.json()
    # Check that the response contains an authentication token and correct email
    assert "token" in data
    assert data["email"] == test_user["email"]
    # Update client headers with the Bearer token for authorized requests
    client.headers.update({"Authorization": f"Bearer {data['token']}"})


@pytest.mark.asyncio
async def test_get_me(client):
    # Register the test user to ensure it exists
    await client.post("/api/users", json=test_user)
    # Log in to receive a token for authentication
    login_response = await client.post(
        "/api/users/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert login_response.status_code == 200  # Confirm successful login
    token = login_response.json()["token"]

    # Prepare authorization header with the token
    headers = {"Authorization": f"Bearer {token}"}
    # Access the protected /me endpoint with authorization
    response = await client.get("/api/users/me", headers=headers)

    assert response.status_code == 200  # Expect HTTP 200 OK
    data = response.json()
    # Verify returned user data matches test user data
    assert data["email"] == test_user["email"]
    assert data["login"] == test_user["login"]
    assert "id" in data  # The response should contain a user ID
