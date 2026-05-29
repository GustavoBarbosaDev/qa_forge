# ============================================================
#  QA Forge — Testes de API: Recurso User
#  Cobre: criação, login, consulta, atualização e remoção.
# ============================================================

import pytest

from src.api.clients.user_client import UserClient
from support.factories.data_factory import UserFactory


@pytest.mark.api
class TestCrudUser:
    """Valida as operações CRUD do endpoint /user."""

    def test_criar_usuario_retorna_sucesso(self, user_client: UserClient):
        """POST /user deve retornar código de sucesso."""
        payload = UserFactory.novo_usuario()

        resposta = user_client.criar_usuario(payload)

        user_client.assert_status(resposta, 200)
        # Limpeza manual pois não usamos a fixture com teardown aqui
        user_client.remover_usuario(payload["username"])

    def test_buscar_usuario_criado(
        self, user_client: UserClient, usuario_criado: dict
    ):
        """GET /user/{username} deve retornar o usuário recém-criado."""
        resposta = user_client.buscar_usuario(usuario_criado["username"])

        user_client.assert_status(resposta, 200)
        assert resposta.json()["username"] == usuario_criado["username"]

    def test_atualizar_email_do_usuario(
        self, user_client: UserClient, usuario_criado: dict
    ):
        """PUT /user/{username} deve refletir o novo email."""
        novo_email = "forge_atualizado@teste.com"
        usuario_criado["email"] = novo_email

        resposta = user_client.atualizar_usuario(
            usuario_criado["username"], usuario_criado
        )
        user_client.assert_status(resposta, 200)

    def test_remover_usuario_existente(self, user_client: UserClient):
        """DELETE /user/{username} deve remover o usuário com sucesso."""
        payload = UserFactory.novo_usuario()
        user_client.criar_usuario(payload)

        resposta = user_client.remover_usuario(payload["username"])
        user_client.assert_status(resposta, 200)

    def test_buscar_usuario_inexistente_retorna_404(self, user_client: UserClient):
        """GET /user/{username} com nome inválido deve retornar 404."""
        resposta = user_client.buscar_usuario("usuario_que_nao_existe_forge_9999")
        user_client.assert_status(resposta, 404)


@pytest.mark.api
class TestAutenticacaoUser:
    """Valida o fluxo de login e logout."""

    def test_login_com_credenciais_validas(
        self, user_client: UserClient, usuario_criado: dict
    ):
        """GET /user/login deve retornar token de sessão no header."""
        resposta = user_client.login(
            usuario_criado["username"], usuario_criado["password"]
        )
        user_client.assert_status(resposta, 200)
        # A API retorna o token como texto no body
        assert "logged in user session" in resposta.json().get("message", "").lower()

    def test_logout_retorna_sucesso(self, user_client: UserClient):
        """GET /user/logout deve encerrar a sessão com sucesso."""
        resposta = user_client.logout()
        user_client.assert_status(resposta, 200)

    def test_criar_usuarios_em_lote(self, user_client: UserClient):
        """POST /user/createWithArray deve criar múltiplos usuários."""
        usuarios = [UserFactory.novo_usuario() for _ in range(3)]

        resposta = user_client.criar_usuarios_em_lote(usuarios)
        user_client.assert_status(resposta, 200)

        # Limpeza
        for u in usuarios:
            user_client.remover_usuario(u["username"])
