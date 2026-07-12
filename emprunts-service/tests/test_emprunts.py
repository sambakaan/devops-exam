import uuid
from datetime import datetime, timedelta, timezone

import httpx


def _livre_payload(livre_id, quantite_disponible):
    return {
        "id": str(livre_id),
        "titre": "1984",
        "auteur": "George Orwell",
        "isbn": "978-0-452-28423-4",
        "quantite_totale": 3,
        "quantite_disponible": quantite_disponible,
        "date_ajout": "2026-01-01T00:00:00Z",
    }


def _utilisateur_payload(utilisateur_id):
    return {
        "id": str(utilisateur_id),
        "nom": "Doe",
        "prenom": "Jane",
        "email": "jane@example.com",
        "type_utilisateur": "etudiant",
        "date_creation": "2026-01-01T00:00:00Z",
    }


def _mock_emprunt_nominal(respx_mock, livre_id, utilisateur_id, quantite_disponible=3):
    respx_mock.get(f"http://livres-service:8002/livres/{livre_id}").mock(
        return_value=httpx.Response(200, json=_livre_payload(livre_id, quantite_disponible))
    )
    respx_mock.get(f"http://utilisateurs-service:8001/users/{utilisateur_id}").mock(
        return_value=httpx.Response(200, json=_utilisateur_payload(utilisateur_id))
    )
    respx_mock.put(f"http://livres-service:8002/livres/{livre_id}").mock(
        return_value=httpx.Response(200, json=_livre_payload(livre_id, quantite_disponible - 1))
    )


def test_creer_emprunt_nominal(client, auth_headers, respx_mock):
    livre_id = uuid.uuid4()
    utilisateur_id = uuid.uuid4()
    _mock_emprunt_nominal(respx_mock, livre_id, utilisateur_id)

    response = client.post(
        "/emprunts",
        json={"livre_id": str(livre_id), "utilisateur_id": str(utilisateur_id)},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["livre_id"] == str(livre_id)
    assert body["utilisateur_id"] == str(utilisateur_id)
    assert body["statut"] == "en_cours"
    assert body["date_retour_effective"] is None


def test_creer_emprunt_livre_indisponible(client, auth_headers, respx_mock):
    livre_id = uuid.uuid4()
    utilisateur_id = uuid.uuid4()
    respx_mock.get(f"http://livres-service:8002/livres/{livre_id}").mock(
        return_value=httpx.Response(200, json=_livre_payload(livre_id, quantite_disponible=0))
    )

    response = client.post(
        "/emprunts",
        json={"livre_id": str(livre_id), "utilisateur_id": str(utilisateur_id)},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_creer_emprunt_livre_inexistant(client, auth_headers, respx_mock):
    livre_id = uuid.uuid4()
    utilisateur_id = uuid.uuid4()
    respx_mock.get(f"http://livres-service:8002/livres/{livre_id}").mock(
        return_value=httpx.Response(404, json={"detail": "Livre introuvable"})
    )

    response = client.post(
        "/emprunts",
        json={"livre_id": str(livre_id), "utilisateur_id": str(utilisateur_id)},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_retourner_emprunt_nominal(client, auth_headers, respx_mock):
    livre_id = uuid.uuid4()
    utilisateur_id = uuid.uuid4()
    _mock_emprunt_nominal(respx_mock, livre_id, utilisateur_id)

    created = client.post(
        "/emprunts",
        json={"livre_id": str(livre_id), "utilisateur_id": str(utilisateur_id)},
        headers=auth_headers,
    ).json()

    response = client.put(f"/emprunts/{created['id']}/retour", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["statut"] == "retourne"
    assert body["date_retour_effective"] is not None


def test_retourner_emprunt_deja_retourne(client, auth_headers, respx_mock):
    livre_id = uuid.uuid4()
    utilisateur_id = uuid.uuid4()
    _mock_emprunt_nominal(respx_mock, livre_id, utilisateur_id)

    created = client.post(
        "/emprunts",
        json={"livre_id": str(livre_id), "utilisateur_id": str(utilisateur_id)},
        headers=auth_headers,
    ).json()

    client.put(f"/emprunts/{created['id']}/retour", headers=auth_headers)
    response = client.put(f"/emprunts/{created['id']}/retour", headers=auth_headers)
    assert response.status_code == 409


def test_emprunts_en_retard(client, auth_headers, db_session):
    from app.models import Emprunt, StatutEmprunt

    emprunt = Emprunt(
        livre_id=uuid.uuid4(),
        utilisateur_id=uuid.uuid4(),
        statut=StatutEmprunt.en_cours,
        date_retour_prevue=datetime.now(timezone.utc) - timedelta(days=1),
    )
    db_session.add(emprunt)
    db_session.commit()

    response = client.get("/emprunts/retards", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["statut"] == "en_retard"
