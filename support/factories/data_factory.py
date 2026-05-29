# ============================================================
#  QA Forge — Fábrica de Dados de Teste
#  Usa Faker para gerar payloads realistas e únicos a cada run.
#  Centralizar aqui evita dados hardcoded espalhados nos testes.
# ============================================================

from __future__ import annotations

import random

from faker import Faker

# Instância com localização pt_BR para nomes/endereços mais realistas
_fake = Faker("pt_BR")
Faker.seed(0)   # seed=0 → reprodutível; remova para aleatoriedade total


class PetFactory:
    """Gera payloads prontos para o endpoint /pet."""

    STATUS_VALIDOS = ("available", "pending", "sold")

    @classmethod
    def novo_pet(
        cls,
        *,
        pet_id: int | None = None,
        status: str = "available",
    ) -> dict:
        """
        Retorna um dict completo compatível com o schema do Petstore.

        >>> payload = PetFactory.novo_pet()
        >>> assert "name" in payload
        """
        return {
            "id": pet_id or random.randint(100_000, 999_999),
            "category": {
                "id": random.randint(1, 10),
                "name": _fake.word().capitalize(),
            },
            "name": _fake.first_name(),
            "photoUrls": [_fake.image_url()],
            "tags": [
                {"id": random.randint(1, 50), "name": _fake.color_name()}
            ],
            "status": status,
        }


class StoreFactory:
    """Gera payloads prontos para o endpoint /store/order."""

    @classmethod
    def novo_pedido(cls, *, pet_id: int, order_id: int | None = None) -> dict:
        return {
            "id": order_id or random.randint(1, 10),
            "petId": pet_id,
            "quantity": random.randint(1, 5),
            "shipDate": "2025-01-01T00:00:00.000Z",
            "status": "placed",
            "complete": False,
        }


class UserFactory:
    """Gera payloads prontos para o endpoint /user."""

    @classmethod
    def novo_usuario(cls) -> dict:
        """Cria um usuário com dados únicos gerados pelo Faker."""
        primeiro = _fake.first_name()
        ultimo = _fake.last_name()
        return {
            "id": random.randint(10_000, 99_999),
            "username": f"{primeiro.lower()}_{ultimo.lower()}_{random.randint(10,99)}",
            "firstName": primeiro,
            "lastName": ultimo,
            "email": _fake.email(),
            "password": _fake.password(length=12),
            "phone": _fake.phone_number(),
            "userStatus": 1,
        }
