# ============================================================
#  QA Forge — Page Object: Carrinho (SauceDemo)
#  URL: https://www.saucedemo.com/cart.html
# ============================================================

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.web.pages.base_page import ForgePage


class CarrinhoPage(ForgePage):
    """Representa a página do carrinho de compras."""

    _TITULO_PAGINA   = (By.CLASS_NAME, "title")
    _ITENS_NO_CARRINHO = (By.CLASS_NAME, "cart_item")
    _BOTAO_CHECKOUT  = (By.ID, "checkout")
    _BOTAO_CONTINUAR = (By.ID, "continue-shopping")

    # ------------------------------------------------------------------
    # Verificações de estado
    # ------------------------------------------------------------------

    def esta_no_carrinho(self) -> bool:
        return self.aguardar_url_conter("cart")

    def quantidade_de_itens_no_carrinho(self) -> int:
        return len(self.listar_elementos(self._ITENS_NO_CARRINHO))

    def carrinho_esta_vazio(self) -> bool:
        return self.quantidade_de_itens_no_carrinho() == 0

    # ------------------------------------------------------------------
    # Ações de navegação
    # ------------------------------------------------------------------

    def prosseguir_para_checkout(self) -> None:
        self.clicar(self._BOTAO_CHECKOUT)

    def continuar_comprando(self) -> None:
        self.clicar(self._BOTAO_CONTINUAR)
