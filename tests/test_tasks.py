async def test_requires_authentication(client):
    response=await client.get("/tasks/")
    assert response.status_code==401

async def test_create_task(client, auth_headers):
    response=await client.post(
        "/tasks/", json={"title":"Write tests", "description":"Cover CRUD"}, headers=auth_headers
    )

    assert response.status_code==201
    assert response.json()['status']=='todo'

async def test_list_returns_only_own_tasks(client, auth_headers):
    await client.post("/tasks/", json={"title":"Mine"}, headers=auth_headers)
    response=await client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Mine"]


async def test_partial_update_changes_only_sent_field(client, auth_headers):
    created = await client.post(
        "/tasks/", json={"title": "Original", "description": "Keep me"}, headers=auth_headers
    )
    task_id = created.json()["id"]

    response = await client.patch(f"/tasks/{task_id}", json={"status": "done"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["title"] == "Original"
    assert response.json()["description"] == "Keep me"


async def test_delete_task(client, auth_headers):
    created = await client.post("/tasks/", json={"title": "Temporary"}, headers=auth_headers)
    task_id = created.json()["id"]

    assert (await client.delete(f"/tasks/{task_id}", headers=auth_headers)).status_code == 204
    assert (await client.get(f"/tasks/{task_id}", headers=auth_headers)).status_code == 404


async def test_cannot_touch_another_users_task(client, auth_headers, make_headers):
    created = await client.post("/tasks/", json={"title": "Private"}, headers=auth_headers)
    task_id = created.json()["id"]

    attacker = await make_headers()

    assert (await client.get(f"/tasks/{task_id}", headers=attacker)).status_code == 404
    assert (await client.patch(f"/tasks/{task_id}", json={"status": "done"}, headers=attacker)).status_code == 404
    assert (await client.delete(f"/tasks/{task_id}", headers=attacker)).status_code == 404

    # the real owner's task is untouched
    assert (await client.get(f"/tasks/{task_id}", headers=auth_headers)).status_code == 200