import pytest

test_user = {
    "email": "test_board_user@example.com",
    "login": "boarduser",
    "password": "StrongPass123",
}


@pytest.mark.asyncio
async def test_create_board(client):
    # Ensure user exists by registering before login
    await client.post("/api/users", json=test_user)
    # Test user login endpoint
    response = await client.post(
        "/api/users/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    token = response.json()["token"]

    auth_headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/boards/",
        json={"title": "Board 1", "description": "Board for sprint planning tasks"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Board 1"
    assert "id" in data
    global board_id
    board_id = data["id"]


# @pytest.mark.asyncio
# async def test_get_board(client):
#     await client.post("/api/users", json=test_user)
#
#     response = await client.post(
#         "/api/users/login",
#         json={"email": test_user["email"], "password": test_user["password"]},
#     )
#     assert response.status_code == 200
#     token = response.json()["token"]
#
#     auth_headers = {"Authorization": f"Bearer {token}"}
#     response = await client.get(f"/boards/{board_id}", headers=auth_headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == board_id
#     assert data["title"] == "Board 1"
