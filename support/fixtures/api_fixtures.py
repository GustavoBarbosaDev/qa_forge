# ============================================================
#  QA Forge — Fixtures de API
#  Fixtures com teardown garantem limpeza automática após
#  cada teste, mantendo o ambiente de testes isolado e limpo.
# ============================================================

from __future__ import annotations

import pytest

from src.api.clients.pet_client import PetClient
from src.api.clients.store_client import StoreClient
from src.api.clients.user_client import UserClient
from support.factories.data_factory import PetFactory, StoreFactory, UserFactory


# ------------------------------------------------------------------
# Clientes (scope=session → uma instância reutilizada por toda a suíte)
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def pet_client() -> PetClient:
    """Instância única de PetClient compartilhada na sessão de testes."""
    return PetClient()


@pytest.fixture(scope="session")
def store_client() -> StoreClient:
    return StoreClient()


@pytest.fixture(scope="session")
def user_client() -> UserClient:
    return UserClient()


# ------------------------------------------------------------------
# Fixture de Pet com teardown automático
# ------------------------------------------------------------------

@pytest.fixture
def pet_criado(pet_client: PetClient) -> dict:
    """
    Cria um pet via API antes do teste e o remove ao final.

    Uso:
        def test_algo(pet_criado):
            assert pet_criado["name"] != ""
    """
    payload = PetFactory.novo_pet()
    resposta = pet_client.criar_pet(payload)
    assert resposta.status_code == 200, "Pré-condição falhou: não foi possível criar o pet"

    pet = resposta.json()
    yield pet  # ← aqui o teste roda

    # Teardown: apaga o pet mesmo que o teste falhe
    pet_client.deletar_pet(pet["id"])


# ------------------------------------------------------------------
# Fixture de Pedido com teardown automático
# ------------------------------------------------------------------

@pytest.fixture
def pedido_criado(pet_criado: dict, store_client: StoreClient) -> dict:
    """Cria um pedido para o pet gerado pela fixture `pet_criado`."""
    payload = StoreFactory.novo_pedido(pet_id=pet_criado["id"])
    resposta = store_client.criar_pedido(payload)
    assert resposta.status_code == 200, "Pré-condição falhou: não foi possível criar o pedido"

    pedido = resposta.json()
    yield pedido

    # Teardown: tenta cancelar o pedido; ignora se já não existir
    store_client.cancelar_pedido(pedido["id"])


# ------------------------------------------------------------------
# Fixture de Usuário com teardown automático
# ------------------------------------------------------------------

@pytest.fixture
def usuario_criado(user_client: UserClient) -> dict:
    """Cria um usuário aleatório e o remove após o teste."""
    payload = UserFactory.novo_usuario()
    resposta = user_client.criar_usuario(payload)
    assert resposta.status_code == 200, "Pré-condição falhou: não foi possível criar o usuário"

    yield payload  # retornamos o payload pois a API não devolve o objeto completo

    user_client.remover_usuario(payload["username"])
