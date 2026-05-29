# ============================================================
#  QA Forge — Fixtures Web (Selenium + Chromium Snap)
#  Gerencia o ciclo de vida do WebDriver: abre antes do teste,
#  tira screenshot em falha e fecha ao finalizar.
# ============================================================

from __future__ import annotations

import os
import tempfile
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _montar_opcoes_chrome(headless: bool) -> ChromeOptions:
    opcoes = ChromeOptions()
    if headless:
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1920,1080")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    # Snap restringe escrita no temp padrão; /tmp é sempre acessível
    opcoes.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    return opcoes


@pytest.fixture(scope="function")
def driver(request):
    modo_headless = os.getenv("HEADLESS", "true").lower() == "true"
    opcoes = _montar_opcoes_chrome(headless=modo_headless)

    driver_path = ChromeDriverManager().install()
    driver_dir = os.path.dirname(driver_path)
    if os.path.basename(driver_path).startswith("THIRD_PARTY_NOTICES"):
        driver_path = os.path.join(driver_dir, "chromedriver.exe")

    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"ChromeDriver não encontrado: {driver_path}")

    navegador = webdriver.Chrome(
        service=Service(driver_path),
        options=opcoes,
    )

    yield navegador  # ← o teste roda aqui

    # ------------------------------------------------------------------
    # Teardown: screenshot em falha + fechar navegador
    # ------------------------------------------------------------------
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        pasta = "reports/screenshots"
        os.makedirs(pasta, exist_ok=True)
        nome_arquivo = f"{pasta}/{request.node.name}.png"
        navegador.save_screenshot(nome_arquivo)

    navegador.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook necessário para o teardown do driver acessar o resultado do teste."""
    resultado = yield
    item.rep_call = resultado.get_result() if call.when == "call" else None
