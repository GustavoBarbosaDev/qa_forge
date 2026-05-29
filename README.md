# 🔬 QA Forge

> Projeto de automação de testes profissional com Python, Pytest, Selenium e GitHub Actions.

---

## 🗂️ Estrutura de Pastas

```
qa_forge/
│
├── .github/
│   └── workflows/
│       └── qa_forge_pipeline.yml   # Pipeline de CI/CD
│
├── src/                            # Código-fonte de automação
│   ├── api/
│   │   ├── clients/
│   │   │   ├── base_client.py      # Cliente HTTP base (herança)
│   │   │   ├── pet_client.py       # Endpoint /pet
│   │   │   ├── store_client.py     # Endpoint /store
│   │   │   └── user_client.py      # Endpoint /user
│   │   └── schemas/                # (opcional) JSONSchemas para validação
│   └── web/
│       ├── pages/
│       │   ├── base_page.py        # Base Page (POM) — métodos Selenium compartilhados
│       │   ├── login_page.py
│       │   ├── inventory_page.py
│       │   ├── cart_page.py
│       │   └── checkout_page.py
│       └── flows/
│           └── fluxo_de_compra.py  # Orquestrador E2E
│
├── support/                        # Infraestrutura de suporte
│   ├── factories/
│   │   └── data_factory.py         # Faker: geração de dados dinâmicos
│   └── fixtures/
│       ├── api_fixtures.py         # Fixtures de API com teardown
│       └── web_fixtures.py         # Fixtures do Selenium com teardown
│
├── tests/                          # Suítes de testes
│   ├── api/
│   │   ├── pet/test_pet.py
│   │   ├── store/test_store.py
│   │   └── user/test_user.py
│   └── web/
│       └── test_saucedemo.py
│
├── reports/                        # Gerado em runtime (ignorado pelo git)
├── conftest.py                     # Carrega fixtures globalmente
├── pytest.ini                      # Configuração central do Pytest
└── requirements.txt
```

---

## 🚀 Instalação e Execução Local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/qa-forge.git
cd qa-forge

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute todos os testes
pytest

# 5. Execute apenas os testes de API
pytest -m api

# 6. Execute apenas os testes Web
pytest -m web

# 7. Execute em modo visual (sem headless)
HEADLESS=false pytest -m web
```

---

## 🏗️ Decisões de Arquitetura

| Conceito | Implementação | Motivo |
|---|---|---|
| **POM + Base Page** | `ForgePage` → `LoginPage`, `InventarioPage`... | Evita duplicação de métodos Selenium |
| **Fixtures com teardown** | `yield` + remoção via API | Garante isolamento entre testes |
| **Data Factory + Faker** | `PetFactory`, `UserFactory`... | Dados únicos por run; sem hardcode |
| **Clientes HTTP com herança** | `ForgeHttpClient` → `PetClient`... | Centraliza sessão e validações |
| **Fluxo E2E separado** | `FluxoDeCompra` em `/flows` | Reutilização de cenários complexos |
| **Marcadores Pytest** | `@pytest.mark.api` / `@pytest.mark.web` | Execução seletiva em CI |

---

## 📊 CI/CD — GitHub Actions

O pipeline é dividido em **3 jobs paralelos**:

```
Push / PR
    │
    ├── [Job 1] testes-api    ──→ relatorio-api-N.html (artefato)
    │
    ├── [Job 2] testes-web    ──→ relatorio-web-N.html (artefato)
    │                              screenshots/ (em caso de falha)
    │
    └── [Job 3] relatorio-consolidado  (depende dos dois anteriores)
```

---

## 🧰 Tecnologias

- **Python 3.11+** — linguagem principal
- **Pytest 8** — framework de testes
- **Selenium 4** + **WebDriver Manager** — automação Web
- **Requests** — testes de API
- **Faker** — geração de dados dinâmicos
- **pytest-html** — relatórios HTML
- **GitHub Actions** — CI/CD
