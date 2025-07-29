from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

#para poder usar variaveis de ambiente dentro do codigo
load_dotenv()

#pegando uma variavel de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

#consfiguração para poder usar o bcrypt para criptografar as informações que vão para o banco de dados
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_shema = OAuth2PasswordBearer(tokenUrl="auth/login_form")


from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para rodar nosse codigo, executar no terminal: uvicorn main:app --reload