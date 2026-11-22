
import pytest

from src.desconto import calcular_desconto, calcular_frete

@pytest.mark.parametrize(
    "valor, esperado",
    [
        (0, 0.0),
        (99.99, 99.99),
        (100.0, 90.0),
        (200.0, 180.0),
    ],
)
def test_calcular_desconto_valores_limite(valor, esperado):
    resultado = calcular_desconto(valor)
    assert resultado == esperado

def test_calcular_desconto_valor_negativo():
    with pytest.raises(ValueError):
        calcular_desconto(-10)

def test_calcular_frete_gratis():
    resultado = calcular_frete(200, 10)
    assert resultado == 0.0

def test_calcular_frete_com_distancia():
    resultado = calcular_frete(100, 10)
    assert resultado == 25.0

def test_calcular_frete_pedido_negativo():
    with pytest.raises(ValueError):
        calcular_frete(-10, 5)

def test_calcular_frete_distancia_negativa():
    with pytest.raises(ValueError):
        calcular_frete(100, -5)