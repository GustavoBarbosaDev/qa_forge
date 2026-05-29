# ============================================================
#  QA Forge — Page Object: Inventário (SauceDemo)
#  URL: https://www.saucedemo.com/inventory.html
# ============================================================

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.web.pages.base_page import ForgePage


class InventarioPage(ForgePage):
    """Representa a página de listagem de produtos."""

    _TITULO_PAGINA  = (By.CLASS_NAME, "title")
    _ITENS_DO_MENU  = (By.CLASS_NAME, "inventory_item")
    _BOTOES_ADICIONAR = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    _ICONE_CARRINHO = (By.CLASS_NAME, "shopping_cart_link")
    _BADGE_CARRINHO = (By.CLASS_NAME, "shopping_cart_badge")
    _MENU_HAMBURGUER = (By.ID, "react-burger-menu-btn")
    _LINK_LOGOUT    = (By.ID, "logout_sidebar_link")

    # ------------------------------------------------------------------
    # Verificações de estado
    # ------------------------------------------------------------------

    def esta_na_pagina_de_inventario(self) -> bool:
        return self.aguardar_url_conter("inventory")

    def titulo_visivel(self) -> str:
        return self.ler_texto(self._TITULO_PAGINA)

    def quantidade_de_produtos(self) -> int:
        return len(self.listar_elementos(self._ITENS_DO_MENU))

    # ------------------------------------------------------------------
    # Ações de compra
    # ------------------------------------------------------------------

    def adicionar_primeiro_produto(self) -> "InventarioPage":
        """Clica em 'Add to cart' no primeiro produto da lista."""
        botoes = self.listar_elementos(self._BOTOES_ADICIONAR)
        assert botoes, "Nenhum produto disponível para adicionar"
        botoes[0].click()
        return self

    def adicionar_produto_por_indice(self, indice: int) -> "InventarioPage":
        """Adiciona o produto pelo índice (base 0) da listagem."""
        botoes = self.listar_elementos(self._BOTOES_ADICIONAR)
        botoes[indice].click()
        return self

    def quantidade_no_badge_do_carrinho(self) -> int:
        """Retorna a quantidade exibida no badge do ícone do carrinho."""
        if not self.elemento_esta_presente(self._BADGE_CARRINHO):
            return 0
        return int(self.ler_texto(self._BADGE_CARRINHO))

    def ir_para_carrinho(self) -> None:
        self.clicar(self._ICONE_CARRINHO)

    def fazer_logout(self) -> None:
        self.clicar(self._MENU_HAMBURGUER)
        self.clicar(self._LINK_LOGOUT)
