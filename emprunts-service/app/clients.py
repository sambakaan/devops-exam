import os

import httpx
from dotenv import load_dotenv

load_dotenv()

LIVRES_SERVICE_URL = os.getenv("LIVRES_SERVICE_URL")
UTILISATEURS_SERVICE_URL = os.getenv("UTILISATEURS_SERVICE_URL")

TIMEOUT = 5.0


class LivreIntrouvableError(Exception):
    pass


class UtilisateurIntrouvableError(Exception):
    pass


class ServiceExterneIndisponibleError(Exception):
    pass


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_livre(livre_id, token: str) -> dict:
    url = f"{LIVRES_SERVICE_URL}/livres/{livre_id}"
    try:
        response = httpx.get(url, headers=_headers(token), timeout=TIMEOUT)
    except httpx.RequestError as exc:
        raise ServiceExterneIndisponibleError(f"livres-service injoignable : {exc}") from exc

    if response.status_code == 404:
        raise LivreIntrouvableError(f"Livre {livre_id} introuvable")
    if response.status_code >= 400:
        raise ServiceExterneIndisponibleError(
            f"livres-service a répondu {response.status_code} pour GET /livres/{livre_id}"
        )
    return response.json()


def update_livre_quantite(livre_id, quantite_disponible: int, token: str) -> dict:
    url = f"{LIVRES_SERVICE_URL}/livres/{livre_id}"
    try:
        response = httpx.put(
            url, json={"quantite_disponible": quantite_disponible}, headers=_headers(token), timeout=TIMEOUT
        )
    except httpx.RequestError as exc:
        raise ServiceExterneIndisponibleError(f"livres-service injoignable : {exc}") from exc

    if response.status_code == 404:
        raise LivreIntrouvableError(f"Livre {livre_id} introuvable")
    if response.status_code >= 400:
        raise ServiceExterneIndisponibleError(
            f"livres-service a répondu {response.status_code} pour PUT /livres/{livre_id}"
        )
    return response.json()


def get_utilisateur(user_id, token: str) -> dict:
    url = f"{UTILISATEURS_SERVICE_URL}/users/{user_id}"
    try:
        response = httpx.get(url, headers=_headers(token), timeout=TIMEOUT)
    except httpx.RequestError as exc:
        raise ServiceExterneIndisponibleError(f"utilisateurs-service injoignable : {exc}") from exc

    if response.status_code == 404:
        raise UtilisateurIntrouvableError(f"Utilisateur {user_id} introuvable")
    if response.status_code >= 400:
        raise ServiceExterneIndisponibleError(
            f"utilisateurs-service a répondu {response.status_code} pour GET /users/{user_id}"
        )
    return response.json()
