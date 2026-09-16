import pytest

@pytest.mark.asyncio
async def test_register_new_user(client):
    response = await client.post(
        "/auth/register",
        json={'email':'testuser@example.com', 'password':"SecuredKey"},
    )

    assert response.status_code==201
    data = response.json()
    assert data["email"] =='testuser@example.com'
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email_fails(client):
    await client.post("/auth/register", json={'email':'dup@example.com', 'password':'Pass123'})
    response = await client.post("/auth/register", json={'email':'dup@example.com', 'password':'Pass123'})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={"email": "login@example.com", "password": "Pass123!"})
    response = await client.post("/auth/login", json={"email": "login@example.com", "password": "Pass123!"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password_fails(client):
    await client.post("/auth/register", json={'email':'wrongpass@example.com', 'password':'Correct123'})
    response = await client.post("/auth/login", json={'email':'wrongpass@example.com', 'password':'Wrong123'})
    assert response.status_code==401