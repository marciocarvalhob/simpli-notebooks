import os
from google import genai
from google.genai import types
import json
import re

# Pega a chave do ambiente (Segurança para GitHub)
MINHA_CHAVE = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=MINHA_CHAVE)

def buscar_ofertas():
    print("🔎 Iniciando varredura técnica de mercado...")
    
    instrucao = """
    Aja como um analista de hardware. Busque 5 notebooks IPS no Brasil (R$ 2.500 - 3.800).
    FORMATO JSON OBRIGATÓRIO:
    {
      "melhores_notebooks": [
        {
          "posicao": 1,
          "modelo": "Nome Completo",
          "preco": "R$ 0.000,00",
          "link": "URL real da loja ou deixe vazio se não tiver certeza",
          "foto": "URL direta da imagem",
          "cpu": "Processador",
          "ram": "Memória",
          "ssd": "SSD",
          "tela": "IPS Full HD",
          "analise": "Veredito técnico curto",
          "notas": { "performance": 8, "tela": 9, "custo_beneficio": 10 }
        }
      ]
    }
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction=instrucao,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
            contents="Top 5 notebooks custo-benefício hoje."
        )

        match = re.search(r'(\{.*\})', response.text, re.DOTALL)
        if match:
            dados = json.loads(match.group(1))
            with open('ofertas.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            print("✅ Sucesso: ofertas.json atualizado.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    buscar_ofertas()