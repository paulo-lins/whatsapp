import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analisar_caso_com_ia(texto_cliente: str) -> dict:
    prompt_sistema = (
        "Você é um assistente jurídico de IA especializado em triagem inicial de casos. "
        "Analise o relato do cliente e responda EXTREMAMENTE APENAS em formato JSON válido, "
        "contendo exatamente estas três chaves:\n"
        '1. "area_direito": a área jurídica predominante.\n'
        '2. "resumo_fatos": um resumo conciso dos fatos principais.\n'
        '3. "proximos_passos": sugestão de conduta inicial para o advogado.\n'
        "Não inclua nenhuma formatação markdown como ```json ou textos adicionais fora do JSON."
    )

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": texto_cliente},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )

    resposta_bruta = chat_completion.choices[0].message.content.strip()

    if resposta_bruta.startswith("```"):
        resposta_bruta = resposta_bruta.split("```")[1]
        if resposta_bruta.startswith("json"):
            resposta_bruta = resposta_bruta[4:]
        resposta_bruta = resposta_bruta.strip()

    return json.loads(resposta_bruta)
