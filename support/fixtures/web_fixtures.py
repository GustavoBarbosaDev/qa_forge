from __future__ import annotations

import os
import shutil
import tempfile
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service


def _montar_opcoes_chrome(headless: bool) -> ChromeOptions:
    opcoes = ChromeOptions()
    if headless:
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1920,1080")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    return opcoes


@pytest.fixture(scope="function")
def driver(request):
    modo_headless = os.getenv("HEADLESS", "true").lower() == "true"
    opcoes = _montar_opcoes_chrome(headless=modo_headless)

    # Usa o chromedriver do PATH (CI) ou busca automaticamente
    driver_path = shutil.which("chromedriver") or "chromedriver"

    navegador = webdriver.Chrome(
        service=Service(driver_path),
        options=opcoes,
    )

    yield navegador

    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        pasta = "reports/screenshots"
        os.makedirs(pasta, exist_ok=True)
        navegador.save_screenshot(f"{pasta}/{request.node.name}.png")

    navegador.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    item.rep_call = resultado.get_result() if call.when == "call" else None