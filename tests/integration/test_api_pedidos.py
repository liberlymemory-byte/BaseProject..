
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_check_retorna_200():
    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_criar_pedido_sucesso():
    client = TestClient(app)
    payload = {
        "item": "Notebook",
        "valor": 150.0,
        "distancia_km": 10.0
    }

    resp = client.post("/pedidos", json=payload)

    assert resp.status_code == 201
    assert resp.json()["item"] == "Notebook"
    assert "total_final" in resp.json()


def test_criar_pedido_valor_negativo():
    client = TestClient(app)
    payload = {
        "item": "Notebook",
        "valor": -10.0,
        "distancia_km": 10.0
    }

    resp = client.post("/pedidos", json=payload)

    assert resp.status_code == 400


def test_criar_pedido_item_vazio():
    client = TestClient(app)
    payload = {
        "item": "   ",
        "valor": 150.0,
        "distancia_km": 10.0
    }

    resp = client.post("/pedidos", json=payload)

    assert resp.status_code == 400


def test_listar_pedidos():
    client = TestClient(app)
    payload = {
        "item": "Livro",
        "valor": 150.0,
        "distancia_km": 10.0
    }

    criado = client.post("/pedidos", json=payload)

    assert criado.status_code == 201

    resp = client.get("/pedidos")

    assert resp.status_code == 200
    assert any(
        pedido["item"] == "Livro"
        for pedido in resp.json()
    )
