# ============================================================
#  QA Forge — Cliente do Endpoint /user
#  Cobre: criação, login, consulta, atualização e remoção.
# ============================================================

from __future__ import annotations

import requests

from src.api.clients.base_client import ForgeHttpClient


class UserClient(ForgeHttpClient):
    """Abstrai todas as operações REST do recurso User."""

    _ROOT = "user"

    def criar_usuario(self, payload: dict) -> requests.Response:
        """POST /user."""
        return self._post(self._ROOT, payload)

    def criar_usuarios_em_lote(self, lista: list[dict]) -> requests.Response:
        """POST /user/createWithArray — cadastra múltiplos usuários."""
        return self._post(f"{self._ROOT}/createWithArray", lista)

    def login(self, username: str, password: str) -> requests.Response:
        """GET /user/login — autentica e retorna token de sessão."""
        return self._get(
            f"{self._ROOT}/login",
            params={"username": username, "password": password},
        )

    def logout(self) -> requests.Response:
        """GET /user/logout."""
        return self._get(f"{self._ROOT}/logout")

    def buscar_usuario(self, username: str) -> requests.Response:
        """GET /user/{username}."""
        return self._get(f"{self._ROOT}/{username}")

    def atualizar_usuario(self, username: str, payload: dict) -> requests.Response:
        """PUT /user/{username}."""
        return self._put(f"{self._ROOT}/{username}", payload)

    def remover_usuario(self, username: str) -> requests.Response:
        """DELETE /user/{username}."""
        return self._delete(f"{self._ROOT}/{username}")
