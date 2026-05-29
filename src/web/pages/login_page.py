# ============================================================
#  QA Forge — Page Object: Login (SauceDemo)
#  URL: https://www.saucedemo.com/
# ============================================================

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.web.pages.base_page import ForgePage


class LoginPage(ForgePage):
    """
    Representa a tela de login do SauceDemo.

    Cada método público retorna ``self`` para permitir encadeamento
    fluente:  page.digitar_usuario("x").digitar_senha("y").entrar()
    """

    # ------------------------------------------------------------------
    # Localizadores (privados; nenhum teste acessa o DOM diretamente)
    # ------------------------------------------------------------------
    _CAMPO_USUARIO = (By.ID, "user-name")
    _CAMPO_SENHA   = (By.ID, "password")
    _BOTAO_LOGIN   = (By.ID, "login-button")
    _MENSAGEM_ERRO = (By.CSS_SELECTOR, "[data-test='error']")

    # ------------------------------------------------------------------
    # Ações de negócio
    # ------------------------------------------------------------------

    def abrir_pagina_de_login(self) -> "LoginPage":
        self.abrir()   # usa WEB_BASE_URL do ambiente
        return self

    def preencher_usuario(self, usuario: str) -> "LoginPage":
        self.digitar(self._CAMPO_USUARIO, usuario)
        return self

    def preencher_senha(self, senha: str) -> "LoginPage":
        self.digitar(self._CAMPO_SENHA, senha)
        return self

    def clicar_em_entrar(self) -> None:
        self.clicar(self._BOTAO_LOGIN)

    def fazer_login(self, usuario: str, senha: str) -> None:
        """Atalho: preenche credenciais e submete o formulário."""
        (
            self.abrir_pagina_de_login()
                .preencher_usuario(usuario)
                .preencher_senha(senha)
                .clicar_em_entrar()
        )

    # ------------------------------------------------------------------
    # Verificações de estado
    # ------------------------------------------------------------------

    def mensagem_de_erro(self) -> str:
        return self.ler_texto(self._MENSAGEM_ERRO)

    def erro_esta_visivel(self) -> bool:
        return self.elemento_esta_presente(self._MENSAGEM_ERRO)
