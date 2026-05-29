# ============================================================
#  QA Forge — Base Page (POM)
#  Todos os Page Objects herdam daqui.
#  Centraliza: esperas, cliques, leituras e navegação.
#  Nunca instancie esta classe diretamente nos testes.
# ============================================================

from __future__ import annotations

import os

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ForgePage:
    """
    Camada base do Page Object Model.

    Encapsula interações elementares com o DOM para que páginas
    concretas falem a linguagem do negócio, não do Selenium.

    Exemplo de herança::

        class LoginPage(ForgePage):
            _CAMPO_EMAIL = (By.ID, "user-name")

            def preencher_email(self, valor: str) -> "LoginPage":
                self.digitar(self._CAMPO_EMAIL, valor)
                return self
    """

    # Tempo padrão de espera explícita (segundos)
    _TIMEOUT_PADRAO = 5

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._espera = WebDriverWait(driver, self._TIMEOUT_PADRAO)

    # ------------------------------------------------------------------
    # Navegação
    # ------------------------------------------------------------------

    def abrir(self, url: str | None = None) -> None:
        """Navega para a URL do ambiente ou para uma URL específica."""
        destino = url or os.getenv("WEB_BASE_URL", "")
        self._driver.get(destino)

    @property
    def titulo_da_pagina(self) -> str:
        return self._driver.title

    @property
    def url_atual(self) -> str:
        return self._driver.current_url

    # ------------------------------------------------------------------
    # Interações com Elementos
    # ------------------------------------------------------------------

    def aguardar_visivel(self, localizador: tuple) -> WebElement:
        """Espera o elemento estar visível e o retorna."""
        return self._espera.until(EC.visibility_of_element_located(localizador))

    def aguardar_clicavel(self, localizador: tuple) -> WebElement:
        """Espera o elemento ser clicável e o retorna."""
        return self._espera.until(EC.element_to_be_clickable(localizador))

    def clicar(self, localizador: tuple) -> None:
        """Aguarda clicabilidade e dispara o clique."""
        self.aguardar_clicavel(localizador).click()

    def digitar(self, localizador: tuple, texto: str) -> None:
        """Limpa o campo e digita o texto fornecido."""
        campo = self.aguardar_visivel(localizador)
        campo.clear()
        campo.send_keys(texto)

    def ler_texto(self, localizador: tuple) -> str:
        """Retorna o texto visível do elemento."""
        return self.aguardar_visivel(localizador).text

    def elemento_esta_presente(self, localizador: tuple) -> bool:
        """Verifica se o elemento existe no DOM sem lançar exceção."""
        try:
            self.aguardar_visivel(localizador)
            return True
        except Exception:
            return False

    def aguardar_url_conter(self, fragmento: str) -> bool:
        """Espera até que a URL atual contenha o fragmento informado."""
        return self._espera.until(EC.url_contains(fragmento))

    def listar_elementos(self, localizador: tuple) -> list[WebElement]:
        """Retorna lista de elementos que correspondem ao localizador."""
        self._espera.until(EC.presence_of_all_elements_located(localizador))
        return self._driver.find_elements(*localizador)
