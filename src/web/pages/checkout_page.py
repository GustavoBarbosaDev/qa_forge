# ============================================================
#  QA Forge — Page Objects: Checkout (SauceDemo)
#  Passo 1 → Informações pessoais
#  Passo 2 → Revisão + Confirmação
# ============================================================

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.web.pages.base_page import ForgePage


class CheckoutInfoPage(ForgePage):
    """
    Passo 1 do Checkout: preenchimento de dados de entrega.
    URL: /checkout-step-one.html
    """

    _CAMPO_NOME      = (By.ID, "first-name")
    _CAMPO_SOBRENOME = (By.ID, "last-name")
    _CAMPO_CEP       = (By.ID, "postal-code")
    _BOTAO_CONTINUAR = (By.ID, "continue")
    _BOTAO_CANCELAR  = (By.ID, "cancel")
    _MENSAGEM_ERRO   = (By.CSS_SELECTOR, "[data-test='error']")

    def esta_no_passo_um(self) -> bool:
        return self.aguardar_url_conter("checkout-step-one")

    def preencher_dados_de_entrega(
        self, nome: str, sobrenome: str, cep: str
    ) -> "CheckoutInfoPage":
        self.digitar(self._CAMPO_NOME, nome)
        self.digitar(self._CAMPO_SOBRENOME, sobrenome)
        self.digitar(self._CAMPO_CEP, cep)
        return self

    def continuar(self) -> None:
        self.clicar(self._BOTAO_CONTINUAR)

    def cancelar(self) -> None:
        self.clicar(self._BOTAO_CANCELAR)

    def mensagem_de_erro(self) -> str:
        return self.ler_texto(self._MENSAGEM_ERRO)


class CheckoutReviewPage(ForgePage):
    """
    Passo 2 do Checkout: revisão de pedido e finalização.
    URL: /checkout-step-two.html
    """

    _SUBTOTAL_LABEL  = (By.CLASS_NAME, "summary_subtotal_label")
    _TAX_LABEL       = (By.CLASS_NAME, "summary_tax_label")
    _TOTAL_LABEL     = (By.CLASS_NAME, "summary_total_label")
    _BOTAO_FINALIZAR = (By.ID, "finish")
    _BOTAO_CANCELAR  = (By.ID, "cancel")

    def esta_na_revisao(self) -> bool:
        return self.aguardar_url_conter("checkout-step-two")

    def subtotal(self) -> str:
        return self.ler_texto(self._SUBTOTAL_LABEL)

    def total_com_imposto(self) -> str:
        return self.ler_texto(self._TOTAL_LABEL)

    def finalizar_compra(self) -> None:
        self.clicar(self._BOTAO_FINALIZAR)


class CheckoutConfirmacaoPage(ForgePage):
    """
    Tela de confirmação após a compra ser finalizada.
    URL: /checkout-complete.html
    """

    _TITULO_SUCESSO  = (By.CLASS_NAME, "complete-header")
    _TEXTO_SUCESSO   = (By.CLASS_NAME, "complete-text")
    _BOTAO_VOLTAR    = (By.ID, "back-to-products")

    def compra_confirmada(self) -> bool:
        return self.aguardar_url_conter("checkout-complete")

    def mensagem_de_sucesso(self) -> str:
        return self.ler_texto(self._TITULO_SUCESSO)

    def voltar_para_produtos(self) -> None:
        self.clicar(self._BOTAO_VOLTAR)
