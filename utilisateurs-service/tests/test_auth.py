def _payload(email="samba@example.com"):
    return {
        "nom": "Samba",
        "prenom": "Kane",
        "email": email,
        "mot_de_passe": "motdepasse123",
        "type_utilisateur": "etudiant",
    }


def test_register_nominal(client):
    response = client.post("/auth/register", json=_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "samba@example.com"
    assert "mot_de_passe_hash" not in body
    assert "id" in body


def test_register_email_deja_pris(client):
    client.post("/auth/register", json=_payload())
    response = client.post("/auth/register", json=_payload())
    assert response.status_code == 400


def test_login_nominal(client):
    client.post("/auth/register", json=_payload())
    response = client.post(
        "/auth/login", json={"email": "samba@example.com", "mot_de_passe": "motdepasse123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_mauvais_mot_de_passe(client):
    client.post("/auth/register", json=_payload())
    response = client.post(
        "/auth/login", json={"email": "samba@example.com", "mot_de_passe": "mauvais"}
    )
    assert response.status_code == 401
