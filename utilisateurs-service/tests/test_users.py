import uuid


def _register_and_login(client, email="pape@example.com"):
    client.post(
        "/auth/register",
        json={
            "nom": "pape",
            "prenom": "kane",
            "email": email,
            "mot_de_passe": "motdepasse123",
            "type_utilisateur": "professeur",
        },
    )
    login = client.post("/auth/login", json={"email": email, "mot_de_passe": "motdepasse123"})
    return login.json()["access_token"]


def test_list_users_sans_token(client):
    response = client.get("/users")
    assert response.status_code == 401


def test_list_users_avec_token(client):
    token = _register_and_login(client)
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    emails = [u["email"] for u in response.json()]
    assert "pape@example.com" in emails


def test_get_user_by_id_valide(client):
    token = _register_and_login(client)
    users = client.get("/users", headers={"Authorization": f"Bearer {token}"}).json()
    user_id = users[0]["id"]
    response = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_by_id_inexistant(client):
    token = _register_and_login(client)
    response = client.get(
        f"/users/{uuid.uuid4()}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
