import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Força o carregamento explícito do .env da raiz do projeto
load_dotenv()

# Pega o link do .env ou usa o valor correto como segurança (sem o nome antigo)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password123@127.0.0.1:5432/triagem_juridica"
)

print(f"-> Conectando ao banco usando a URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
