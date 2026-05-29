# ============================================================
#  QA Forge — Testes Web E2E: SauceDemo
#  Cobre: login, inventário, carrinho e checkout completo.
# ============================================================

import pytest

from src.web.flows.fluxo_de_compra import FluxoDeCompra
from src.web.pages.inventory_page import InventarioPage
from src.web.pages.login_page import LoginPage


# ------------------------------------------------------------------
# Credenciais do SauceDemo (valores públicos da documentação)
# ------------------------------------------------------------------
USUARIO_VALIDO   = "standard_user"
SENHA_VALIDA     = "secret_sauce"
USUARIO_BLOQUEADO = "locked_out_user"


@pytest.mark.web
class TestLoginSauceDemo:
    def test_login_com_credenciais_validas_redireciona_para_inventario(self, driver):
        pagina = LoginPage(driver)
        inventario = InventarioPage(driver)

        pagina.fazer_login(USUARIO_VALIDO, SENHA_VALIDA)

        assert inventario.esta_na_pagina_de_inventario()
        assert inventario.titulo_visivel() == "Products"

    def test_login_com_usuario_bloqueado_exibe_mensagem_de_erro(self, driver):
        pagina = LoginPage(driver)

        pagina.fazer_login(USUARIO_BLOQUEADO, SENHA_VALIDA)

        assert pagina.erro_esta_visivel()
        assert "locked out" in pagina.mensagem_de_erro().lower()


@pytest.mark.web
class TestCheckoutE2E:
    def test_compra_completa_exibe_mensagem_de_sucesso(self, driver):
        fluxo = FluxoDeCompra(driver)

        resultado = fluxo.executar_compra_completa(
            usuario=USUARIO_VALIDO,
            senha=SENHA_VALIDA,
            nome="Forge",
            sobrenome="QA",
            cep="01310-100",
        )

        mensagem = resultado.confirmacao.mensagem_de_sucesso()
        assert "thank you" in mensagem.lower()
