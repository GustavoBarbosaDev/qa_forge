# ============================================================
#  QA Forge — Cliente do Endpoint /pet
#  Cobre: criação, consulta, atualização e remoção de pets.
# ============================================================

from __future__ import annotations

import requests

from src.api.clients.base_client import ForgeHttpClient


class PetClient(ForgeHttpClient):
    """Abstrai todas as operações REST do recurso Pet."""

    _ROOT = "pet"

    # ------------------------------------------------------------------
    # Operações CRUD
    # ------------------------------------------------------------------

    def criar_pet(self, payload: dict) -> requests.Response:
        """POST /pet — cadastra um novo pet."""
        return self._post(self._ROOT, payload)

    def buscar_pet_por_id(self, pet_id: int) -> requests.Response:
        """GET /pet/{petId}."""
        return self._get(f"{self._ROOT}/{pet_id}")

    def atualizar_pet(self, payload: dict) -> requests.Response:
        """PUT /pet — atualiza todos os campos de um pet existente."""
        return self._put(self._ROOT, payload)

    def deletar_pet(self, pet_id: int) -> requests.Response:
        """DELETE /pet/{petId}."""
        return self._delete(f"{self._ROOT}/{pet_id}")

    # ------------------------------------------------------------------
    # Consultas por filtro
    # ------------------------------------------------------------------

    def listar_por_status(self, status: str) -> requests.Response:
        """
        GET /pet/findByStatus

        :param status: ``available`` | ``pending`` | ``sold``
        """
        return self._get(f"{self._ROOT}/findByStatus", params={"status": status})

    def listar_por_tags(self, tags: list[str]) -> requests.Response:
        """GET /pet/findByTags — filtra pets por uma lista de tags."""
        return self._get(f"{self._ROOT}/findByTags", params={"tags": tags})
