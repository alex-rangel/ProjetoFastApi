from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["autenticacao"])

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario

def criar_token(id_usuario):
    
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

@auth_router.get("/")
async def home():
    """
    Esse é a rota padrão de autenticação do nosso sistema
    """
    return {
                "mensagem": "Você acessou a rota padrão de autenticação", 
                "autenticado": False
            }
    
@auth_router.post("/criar_conta")
async def criar_conta(usuario: UsuarioSchema, session:Session = Depends(pegar_sessao)):
    usuarioExistente = session.query(Usuario).filter(Usuario.email == usuario.email).first()
    
    if usuarioExistente:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario.senha)
        novo_usuario = Usuario(usuario.nome, usuario.email, senha_criptografada, usuario.ativo, usuario.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario.email}"}
    
@auth_router.post("/login")
async def login(login: LoginSchema, session:Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(login.email, login.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "access_token": acess_token,
            "token_type": "Bearer"
        }
        
@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session:Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credencias inválidas")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "access_token": acess_token,
            "token_type": "Bearer"
        }
        
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    