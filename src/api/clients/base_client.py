# ============================================================
#  QA Forge — Cliente HTTP Base
#  Centraliza a sessão Requests e helpers de asserção de status.
#  Todos os clientes de endpoint herdam daqui.
# ============================================================

from __future__ import annotations

import os
import logging

import requests

logger = logging.getLogger(__name__)


class ForgeHttpClient:
    """
    Camada de transporte compartilhada entre todos os clientes de API.

    Mantém uma única :class:`requests.Session` por instância, o que
    reutiliza conexões TCP e preserva cabeçalhos padrão em todas as
    chamadas.
    """

    # Cabeçalhos enviados em toda requisição — podem ser sobrescritos
    # por clientes filhos ou por testes individuais.
    _DEFAULT_HEADERS: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = (base_url or os.getenv("API_BASE_URL", "")).rstrip("/")
        self._session = requests.Session()
        self._session.headers.update(self._DEFAULT_HEADERS)

    # ------------------------------------------------------------------
    # Métodos HTTP encapsulados
    # ------------------------------------------------------------------

    def _get(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.debug("GET %s", url)
        return self._session.get(url, **kwargs)

    def _post(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.debug("POST %s | body=%s", url, payload)
        return self._session.post(url, json=payload, **kwargs)

    def _put(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.debug("PUT %s | body=%s", url, payload)
        return self._session.put(url, json=payload, **kwargs)

    def _delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.debug("DELETE %s", url)
        return self._session.delete(url, **kwargs)

    # ------------------------------------------------------------------
    # Helpers de validação reutilizáveis nos testes
    # ------------------------------------------------------------------

    @staticmethod
    def assert_status(response: requests.Response, expected: int) -> None:
        """Falha o teste com mensagem clara se o status não bater."""
        actual = response.status_code
        assert actual == expected, (
            f"Status inesperado → esperado {expected}, recebido {actual}.\n"
            f"URL: {response.url}\n"
            f"Corpo: {response.text[:500]}"
        )

    @staticmethod
    def assert_json_key(response: requests.Response, key: str) -> None:
        """Verifica que a chave existe no JSON de resposta."""
        body = response.json()
        assert key in body, (
            f"Chave '{key}' ausente no JSON de resposta.\n"
            f"Chaves presentes: {list(body.keys())}"
        )

    # ------------------------------------------------------------------
    # Utilitário interno
    # ------------------------------------------------------------------

    def _build_url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint.lstrip('/')}"
