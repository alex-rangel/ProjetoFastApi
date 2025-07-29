from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItensSchema, ResponsePedidosSchema
from sqlalchemy.orm import Session
from models import Pedidos, Usuario, ItemPedidos
from dependencies import pegar_sessao, verificar_token
from typing import List

order_router = APIRouter(prefix="/order", tags=["pedidos"], dependencies= [Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisão de autenticação
    """
    return {"mensagem": "você acessou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedidos(usuario=pedido.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    
    return {
        "mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }
    
@order_router.get("/listar")
async def listar_pedidos(session: Session = (Depends(pegar_sessao)), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para esse operação")
    else:
        pedidos = session.query(Pedidos).all()
        return{
            "pedidos": pedidos
        }
        
@order_router.post("pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido: ItensSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para esse operação")
    item_pedido = ItemPedidos(item_pedido.quantidade, item_pedido.sabor, item_pedido.tamanho, item_pedido.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    
    return {
        "mensagem": "Item criado com sucesso",
        "Item_id": item_pedido.id,
        "preço_pedido": pedido.preco
    }
    
@order_router.post("pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedidos).filter(ItemPedidos.id == id_item_pedido).first()
    pedido = session.query(Pedidos).filter(Pedidos.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para esse operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    
    return {
        "mensagem": "Item removido com sucesso",
        "Quantidade_itens_pedido" : len(pedido.itens),
        "pedido": pedido
    }
    
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "FINALIZADO"
    session.commit()
    
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }
    
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = (Depends(pegar_sessao)), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedidos).filter(Pedidos.id==id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }
    
@order_router.get("listar/pedidos-usuario", response_model=List[ResponsePedidosSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedidos).filter(Pedidos.usuario==usuario.id).all()
    return pedidos
