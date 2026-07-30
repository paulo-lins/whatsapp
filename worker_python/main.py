import os

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.core.database import engine
from src.models.models import Base
from src.services.ai_service import analisar_caso_com_ia
from src.workers.tasks import processar_mensagem_whatsapp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = os.path.join(frontend_dir, "index.html")

    if os.path.exists(html_path):
        return FileResponse(html_path)
    return f"<h1>Arquivo index.html não encontrado no caminho: {html_path}</h1>"

Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")

@app.post("/webhook/whatsapp")
@app.post("/webhook/whatsapp/")
async def webhook_whatsapp(payload: dict):
    try:
        texto_cliente = (
            payload.get("entry", [{}])[0]
            .get("changes", [{}])[0]
            .get("value", {})
            .get("messages", [{}])[0]
            .get("text", {})
            .get("body")
        )

        if not texto_cliente:
            texto_cliente = payload.get("message_body") or payload.get("text") or "Olá"

        processar_mensagem_whatsapp.delay(payload)

        resultado_ia = analisar_caso_com_ia(texto_cliente)

        resposta_formatada = (
            f"⚖️ *Área:* {resultado_ia.get('area_direito')}\n\n"
            f"📋 *Resumo:* {resultado_ia.get('resumo_fatos')}\n\n"
            f"💡 *Próximos passos:* {resultado_ia.get('proximos_passos')}"
        )

        return {"status": "sucesso", "mensagem": resposta_formatada}

    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro ao processar a análise: {str(e)}"}
