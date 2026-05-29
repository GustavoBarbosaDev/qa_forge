# ============================================================
#  QA Forge — Testes de API: Recurso Pet
#  Cobre: CRUD completo + consultas por status e tags.
# ============================================================

import pytest

from src.api.clients.pet_client import PetClient
from support.factories.data_factory import PetFactory


@pytest.mark.api
class TestCrudPet:
    """Valida as operações CRUD do endpoint /pet."""

    def test_criar_pet_retorna_201_e_dados_corretos(self, pet_client: PetClient):
        """POST /pet deve retornar 200 com o pet persistido."""
        payload = PetFactory.novo_pet(status="available")

        resposta = pet_client.criar_pet(payload)

        pet_client.assert_status(resposta, 200)
        corpo = resposta.json()
        assert corpo["name"] == payload["name"], (
            f"Nome divergente: esperado '{payload['name']}', recebido '{corpo['name']}'"
        )
        assert corpo["status"] == "available"

    def test_buscar_pet_existente_retorna_dados_completos(
        self, pet_client: PetClient, pet_criado: dict
    ):
        """GET /pet/{id} deve encontrar o pet criado pela fixture."""
        resposta = pet_client.buscar_pet_por_id(pet_criado["id"])

        pet_client.assert_status(resposta, 200)
        assert resposta.json()["id"] == pet_criado["id"]

    def test_atualizar_nome_do_pet(self, pet_client: PetClient, pet_criado: dict):
        """PUT /pet deve refletir o novo nome na resposta."""
        pet_criado["name"] = "NomeForgePremium"
        pet_criado["status"] = "pending"

        resposta = pet_client.atualizar_pet(pet_criado)

        pet_client.assert_status(resposta, 200)
        assert resposta.json()["name"] == "NomeForgePremium"
        assert resposta.json()["status"] == "pending"

    def test_deletar_pet_existente(self, pet_client: PetClient):
        """DELETE /pet/{id} deve remover o pet e retornar 200."""
        payload = PetFactory.novo_pet()
        pet_id = pet_client.criar_pet(payload).json()["id"]

        resposta = pet_client.deletar_pet(pet_id)
        pet_client.assert_status(resposta, 200)

        # Confirma que não existe mais
        resposta_consulta = pet_client.buscar_pet_por_id(pet_id)
        assert resposta_consulta.status_code == 404

    def test_buscar_pet_inexistente_retorna_404(self, pet_client: PetClient):
        """GET /pet/{id} com ID inexistente deve retornar 404."""
        resposta = pet_client.buscar_pet_por_id(999_999_999)
        pet_client.assert_status(resposta, 404)


@pytest.mark.api
class TestConsultasPet:
    """Valida as consultas por filtros do endpoint /pet."""

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_listar_por_status_retorna_lista(
        self, pet_client: PetClient, status: str
    ):
        """GET /pet/findByStatus deve retornar lista não-nula para cada status."""
        resposta = pet_client.listar_por_status(status)

        pet_client.assert_status(resposta, 200)
        resultado = resposta.json()
        assert isinstance(resultado, list), "Resposta deveria ser uma lista"

    def test_todos_os_pets_retornados_tem_status_correto(self, pet_client: PetClient):
        """Garante que o filtro de status funciona corretamente."""
        resposta = pet_client.listar_por_status("available")
        pets = resposta.json()

        pets_incorretos = [p for p in pets if p.get("status") != "available"]
        assert not pets_incorretos, (
            f"{len(pets_incorretos)} pet(s) com status diferente de 'available'"
        )
