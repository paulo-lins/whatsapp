from src.core.celery_app import celery_app
from src.core.database import SessionLocal
from src.models.models import (
    AtendimentoModel,
    MensagemModel,
    StatusAtendimento,
    TipoRemetente,
    UsuarioModel,
)
from src.services.ai_service import analisar_caso_com_ia


@celery_app.task(name="processar_mensagem_whatsapp")
def processar_mensagem_whatsapp(payload):
    # Garante que se vier em formato de lista (por conta do despacho), pegamos o primeiro item
    if isinstance(payload, list) and len(payload) > 0:
        payload = payload[0]

    db = SessionLocal()
    try:
        texto_cliente = payload.get("message_body", "")
        telefone = payload.get("telefone", "+5585999990000")
        nome_usuario = payload.get("nome", "Cliente")

        if not texto_cliente:
            return {"status": "erro", "detalhe": "Mensagem vazia"}

        # 1. Verifica ou cria o usuário no banco
        usuario = (
            db.query(UsuarioModel).filter(UsuarioModel.telefone == telefone).first()
        )
        if not usuario:
            usuario = UsuarioModel(nome=nome_usuario, telefone=telefone)
            db.add(usuario)
            db.commit()
            db.refresh(usuario)

        # 2. Busca atendimento em aberto ou cria um novo
        atendimento = (
            db.query(AtendimentoModel)
            .filter(
                AtendimentoModel.usuario_id == usuario.id,
                AtendimentoModel.status == StatusAtendimento.triagem,
            )
            .first()
        )

        if not atendimento:
            atendimento = AtendimentoModel(
                usuario_id=usuario.id, status=StatusAtendimento.triagem
            )
            db.add(atendimento)
            db.commit()
            db.refresh(atendimento)

        # 3. Salva mensagem do cliente
        msg_cliente = MensagemModel(
            atendimento_id=atendimento.id,
            remetente=TipoRemetente.cliente,
            conteudo=texto_cliente,
        )
        db.add(msg_cliente)
        db.commit()

        # 4. Chama a IA
        resultado_ia = analisar_caso_com_ia(texto_cliente)

        # 5. Atualiza atendimento com os dados da IA
        atendimento.categoria_inferida = resultado_ia.get("area_direito", "N/A")
        atendimento.resumo_ia = resultado_ia.get("resumo_fatos", "N/A")
        db.commit()

        # 6. Formata e salva a resposta do bot
        resposta_formatada = (
            f"⚖️ **Área:** {resultado_ia.get('area_direito', 'N/A')}\n\n"
            f"📄 **Resumo:** {resultado_ia.get('resumo_fatos', 'N/A')}\n\n"
            f"🚀 **Próximos Passos:** {resultado_ia.get('proximos_passos', 'N/A')}"
        )

        msg_bot = MensagemModel(
            atendimento_id=atendimento.id,
            remetente=TipoRemetente.bot,
            conteudo=resposta_formatada,
        )
        db.add(msg_bot)
        db.commit()

        return {"status": "sucesso", "atendimento_id": atendimento.id}

    finally:
        db.close()
