# ============================================================
#  QA Forge — Raiz de Configuração
#  conftest.py carregado automaticamente pelo Pytest em toda
#  a suíte; expõe fixtures globais acessíveis por qualquer teste.
# ============================================================

import pytest

from support.fixtures.api_fixtures import *   # noqa: F401,F403
from support.fixtures.web_fixtures import *   # noqa: F401,F403
