def _payload(isbn="978-2-1234-5680-1"):
    return {"titre": "Le Petit Prince", "auteur": "Antoine de Saint-Exupéry", "isbn": isbn, "quantite_totale": 3}


def test_create_livre_nominal(client, auth_headers):
    response = client.post("/livres", json=_payload(), headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["isbn"] == "978-2-1234-5680-1"
    assert body["quantite_disponible"] == 3
    assert body["quantite_totale"] == 3


def test_create_livre_isbn_deja_pris(client, auth_headers):
    client.post("/livres", json=_payload(), headers=auth_headers)
    response = client.post("/livres", json=_payload(), headers=auth_headers)
    assert response.status_code == 400


def test_create_livre_sans_jwt(client):
    response = client.post("/livres", json=_payload())
    assert response.status_code == 401


def test_get_livre_by_id_sans_jwt(client, auth_headers):
    created = client.post("/livres", json=_payload(), headers=auth_headers).json()
    response = client.get(f"/livres/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_livre_by_id_inexistant(client, auth_headers):
    import uuid

    response = client.get(f"/livres/{uuid.uuid4()}")
    assert response.status_code == 404


def test_list_livres(client, auth_headers):
    client.post("/livres", json=_payload(), headers=auth_headers)
    response = client.get("/livres", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_livre(client, auth_headers):
    created = client.post("/livres", json=_payload(), headers=auth_headers).json()
    response = client.put(
        f"/livres/{created['id']}", json={"quantite_disponible": 1}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["quantite_disponible"] == 1


def test_update_livre_quantite_disponible_ne_depasse_pas_totale(client, auth_headers):
    created = client.post("/livres", json=_payload(), headers=auth_headers).json()
    response = client.put(
        f"/livres/{created['id']}", json={"quantite_disponible": 999}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["quantite_disponible"] == created["quantite_totale"]


def test_update_livre_inexistant(client, auth_headers):
    import uuid

    response = client.put(f"/livres/{uuid.uuid4()}", json={"titre": "X"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_livre(client, auth_headers):
    created = client.post("/livres", json=_payload(), headers=auth_headers).json()
    response = client.delete(f"/livres/{created['id']}", headers=auth_headers)
    assert response.status_code == 204
    assert client.get(f"/livres/{created['id']}").status_code == 404


def test_delete_livre_inexistant(client, auth_headers):
    import uuid

    response = client.delete(f"/livres/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404


def test_search_par_titre(client, auth_headers):
    client.post("/livres", json=_payload(), headers=auth_headers)
    response = client.get("/livres/search?q=Petit Prince", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_par_auteur(client, auth_headers):
    client.post("/livres", json=_payload(), headers=auth_headers)
    response = client.get("/livres/search?q=Exupéry", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_par_isbn(client, auth_headers):
    client.post("/livres", json=_payload(), headers=auth_headers)
    response = client.get("/livres/search?q=978-2-1234-5680-1", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
