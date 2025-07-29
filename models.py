from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

#criar a conexão com o bando de dados
db = create_engine("sqlite:///banco.db")

#criar a base do banco de dados
Base = declarative_base()

#criar as classes / tabelas do banco de dados

#Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)
    
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        
#Pedido
class Pedidos(Base):
    __tablename__ = "pedidos"
    
    # STATUS_PEDIDO = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("stauts", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedidos", cascade="all, delete")
    
    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco
        
    def calcular_preco(self):
        # preco_pedido = 0
        # for item in self.itens:
        #     preco_item = item.preco_unitario * item.quantidade
        #     preco_pedido += preco_item
        
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        
#Itens Pedidos
class ItemPedidos(Base):
    __tablename__ = "itens pedidos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
        

#executa a criação dos metasdados de seu banco de dados (cria eferivamento o banco de dados)

# criar migração: alembic revision --autogenerate -m "nome"
# executar a migração: alembic upgrade head