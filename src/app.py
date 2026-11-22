from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.desconto import calcular_desconto, calcular_frete

app = FastAPI(title="BaseProject - Curso Testes e CI (UNIBRA)")

PEDIDOS_DB: list[dict] = []


class PedidoInput(BaseModel):
    item: str
    valor: float
    distancia_km: float = 0.0


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/pedidos", status_code=201)
def criar_pedido(pedido: PedidoInput):
    if not pedido.item.strip():
        raise HTTPException(status_code=400, detail="Nome do item é obrigatório")

    try:
        total_com_desconto = calcular_desconto(pedido.valor)
        frete = calcular_frete(total_com_desconto, pedido.distancia_km)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err

    novo_pedido = {
        "id": len(PEDIDOS_DB) + 1,
        "item": pedido.item.strip(),
        "valor_original": round(pedido.valor, 2),
        "total_com_desconto": total_com_desconto,
        "frete": frete,
        "total_final": round(total_com_desconto + frete, 2),
    }
    PEDIDOS_DB.append(novo_pedido)
    return novo_pedido


@app.get("/pedidos")
def listar_pedidos():
    return PEDIDOS_DB
