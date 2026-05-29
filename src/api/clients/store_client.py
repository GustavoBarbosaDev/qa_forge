# ============================================================
#  QA Forge — Cliente do Endpoint /store
#  Cobre: inventário, pedidos e remoção de pedidos.
# ============================================================

from __future__ import annotations

import requests

from src.api.clients.base_client import ForgeHttpClient


class StoreClient(ForgeHttpClient):
    """Abstrai todas as operações REST do recurso Store."""

    _ROOT = "store"

    def consultar_inventario(self) -> requests.Response:
        """GET /store/inventory — retorna mapa status→quantidade."""
        return self._get(f"{self._ROOT}/inventory")

    def criar_pedido(self, payload: dict) -> requests.Response:
        """POST /store/order — registra um novo pedido de pet."""
        return self._post(f"{self._ROOT}/order", payload)

    def buscar_pedido_por_id(self, order_id: int) -> requests.Response:
        """GET /store/order/{orderId}."""
        return self._get(f"{self._ROOT}/order/{order_id}")

    def cancelar_pedido(self, order_id: int) -> requests.Response:
        """DELETE /store/order/{orderId}."""
        return self._delete(f"{self._ROOT}/order/{order_id}")
