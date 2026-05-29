# ============================================================
#  QA Forge — Testes de API: Recurso Store
#  Cobre: inventário, criação e cancelamento de pedidos.
# ============================================================

import pytest

from src.api.clients.store_client import StoreClient
from support.factories.data_factory import PetFactory, StoreFactory


@pytest.mark.api
class TestInventarioStore:
    """Valida o endpoint de inventário da loja."""

    def test_inventario_retorna_mapa_de_status(self, store_client: StoreClient):
        """GET /store/inventory deve retornar dict com chaves de status."""
        resposta = store_client.consultar_inventario()

        store_client.assert_status(resposta, 200)
        inventario = resposta.json()
        assert isinstance(inventario, dict), "Inventário deveria ser um dicionário"
        assert len(inventario) > 0, "Inventário não deveria estar vazio"


@pytest.mark.api
class TestPedidosStore:
    """Valida as operações de pedido do endpoint /store/order."""

    def test_criar_pedido_retorna_dados_corretos(
        self, store_client: StoreClient, pet_criado: dict
    ):
        """POST /store/order deve persistir o pedido com o petId informado."""
        payload = StoreFactory.novo_pedido(pet_id=pet_criado["id"])

        resposta = store_client.criar_pedido(payload)

        store_client.assert_status(resposta, 200)
        pedido = resposta.json()
        assert pedido["petId"] == pet_criado["id"]
        assert pedido["status"] == "placed"

    def test_buscar_pedido_por_id(
        self, store_client: StoreClient, pedido_criado: dict
    ):
        """GET /store/order/{id} deve encontrar o pedido criado pela fixture."""
        resposta = store_client.buscar_pedido_por_id(pedido_criado["id"])

        store_client.assert_status(resposta, 200)
        assert resposta.json()["id"] == pedido_criado["id"]

    def test_cancelar_pedido_existente(
        self, store_client: StoreClient, pet_criado: dict
    ):
        """DELETE /store/order/{id} deve remover o pedido com sucesso."""
        payload = StoreFactory.novo_pedido(pet_id=pet_criado["id"])
        pedido_id = store_client.criar_pedido(payload).json()["id"]

        resposta = store_client.cancelar_pedido(pedido_id)
        store_client.assert_status(resposta, 200)

    def test_buscar_pedido_inexistente_retorna_404(self, store_client: StoreClient):
        """GET /store/order/{id} com ID inválido deve retornar 404."""
        resposta = store_client.buscar_pedido_por_id(999_999)
        store_client.assert_status(resposta, 404)
