# ============================================================
#  QA Forge — Fluxo E2E: Compra Completa (SauceDemo)
#  Orquestra Page Objects em sequência para um fluxo de ponta
#  a ponta legível, sem lógica de Selenium no arquivo de teste.
# ============================================================

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from src.web.pages.cart_page import CarrinhoPage
from src.web.pages.checkout_page import (
    CheckoutConfirmacaoPage,
    CheckoutInfoPage,
    CheckoutReviewPage,
)
from src.web.pages.inventory_page import InventarioPage
from src.web.pages.login_page import LoginPage


class FluxoDeCompra:
    """
    Orquestra o fluxo completo: login → produtos → carrinho → checkout.

    Centralizar a sequência aqui permite que múltiplos testes reutilizem
    o mesmo caminho sem duplicar código de navegação.
    """

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        # Instancia todas as páginas necessárias para o fluxo
        self.login     = LoginPage(driver)
        self.inventario = InventarioPage(driver)
        self.carrinho  = CarrinhoPage(driver)
        self.info      = CheckoutInfoPage(driver)
        self.revisao   = CheckoutReviewPage(driver)
        self.confirmacao = CheckoutConfirmacaoPage(driver)

    # ------------------------------------------------------------------
    # Etapas individuais (use nos testes que precisam de granularidade)
    # ------------------------------------------------------------------

    def fazer_login(self, usuario: str, senha: str) -> "FluxoDeCompra":
        self.login.fazer_login(usuario, senha)
        assert self.inventario.esta_na_pagina_de_inventario(), (
            "Login falhou: não redirecionou para o inventário"
        )
        return self

    def adicionar_produto_ao_carrinho(self, indice: int = 0) -> "FluxoDeCompra":
        self.inventario.adicionar_produto_por_indice(indice)
        return self

    def ir_para_carrinho(self) -> "FluxoDeCompra":
        self.inventario.ir_para_carrinho()
        assert self.carrinho.esta_no_carrinho(), "Não foi para a página do carrinho"
        return self

    def prosseguir_para_checkout(self) -> "FluxoDeCompra":
        self.carrinho.prosseguir_para_checkout()
        assert self.info.esta_no_passo_um(), "Não chegou no passo 1 do checkout"
        return self

    def preencher_dados_pessoais(
        self, nome: str, sobrenome: str, cep: str
    ) -> "FluxoDeCompra":
        self.info.preencher_dados_de_entrega(nome, sobrenome, cep)
        self.info.continuar()
        assert self.revisao.esta_na_revisao(), "Não chegou na revisão do pedido"
        return self

    def finalizar_compra(self) -> "FluxoDeCompra":
        self.revisao.finalizar_compra()
        assert self.confirmacao.compra_confirmada(), "Compra não foi confirmada"
        return self

    # ------------------------------------------------------------------
    # Fluxo completo encadeado (uso direto em testes E2E)
    # ------------------------------------------------------------------

    def executar_compra_completa(
        self,
        *,
        usuario: str,
        senha: str,
        nome: str,
        sobrenome: str,
        cep: str,
        indice_produto: int = 0,
    ) -> "FluxoDeCompra":
        """
        Executa do login à confirmação em uma única chamada encadeada.

        Retorna ``self`` para que o teste possa checar o estado final::

            resultado = fluxo.executar_compra_completa(...)
            assert "THANK YOU" in resultado.confirmacao.mensagem_de_sucesso()
        """
        return (
            self.fazer_login(usuario, senha)
                .adicionar_produto_ao_carrinho(indice_produto)
                .ir_para_carrinho()
                .prosseguir_para_checkout()
                .preencher_dados_pessoais(nome, sobrenome, cep)
                .finalizar_compra()
        )
