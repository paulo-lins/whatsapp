from src.core.database import SessionLocal
from src.models.models import AtendimentoModel, MensagemModel, UsuarioModel

# Abre uma conexão rápida com o banco
db = SessionLocal()

try:
    print("\n=================== 📊 DADOS NO POSTGRESQL ===================")

    # 1. Busca Usuários
    usuarios = db.query(UsuarioModel).all()
    print(f"\n👤 USUÁRIOS ENCONTRADOS ({len(usuarios)}):")
    for u in usuarios:
        print(f"  • ID: {u.id} | Nome: {u.nome} | Telefone: {u.telefone}")

    # 2. Busca Atendimentos
    atendimentos = db.query(AtendimentoModel).all()
    print(f"\n📋 ATENDIMENTOS ENCONTRADOS ({len(atendimentos)}):")
    for a in atendimentos:
        print(
            f"  • ID: {a.id} | Usuário ID: {a.usuario_id} | Categoria: {a.categoria_inferida} | Status: {a.status}"
        )

    # 3. Busca Mensagens
    mensagens = db.query(MensagemModel).all()
    print(f"\n💬 MENSAGENS ENCONTRADAS ({len(mensagens)}):")
    for m in mensagens:
        print(f"  • [{m.remetente.value.upper()}]: {m.conteudo[:60]}...")

    print("\n=============================================================\n")

finally:
    db.close()
