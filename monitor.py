from google import genai
from google.genai import types
import json
import re

# 1. CONFIGURAÇÃO - Cole sua chave aqui
MINHA_CHAVE = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=MINHA_CHAVE)

def buscar_ofertas():
    print("🔎 Iniciando varredura técnica (Radar de Custo-Benefício)...")
    
    # Instrução "Dura": Forçamos a IA a dar notas para o gráfico
    instrucao = """
    Aja como um analista de hardware sênior. 
    Busque 5 notebooks IPS no Brasil (R$ 2.500 - R$ 3.800).
    
    REGRAS DO JSON:
    - url_foto: Tente o link da imagem oficial (Samsung, Asus, Dell) ou link direto .jpg/.png.
    - link_direto: URL real da oferta (Amazon, Kabum, Magalu, Mercado Livre).
    - notas: Dê notas de 1 a 10 para Performance, Tela e Custo-Benefício.

    RETORNE APENAS O JSON (SEM MARKDOWN):
    {
      "melhores_notebooks": [
        {
          "posicao": 1,
          "modelo": "Nome do Modelo",
          "preco": "R$ 0.000,00",
          "link": "URL",
          "foto": "URL da Imagem",
          "cpu": "Processador",
          "ram": "Memória",
          "ssd": "Armazenamento",
          "tela": "IPS Full HD",
          "analise": "Resumo técnico curto",
          "notas": { "performance": 8, "tela": 9, "custo_beneficio": 10 }
        }
      ]
    }
    """

    response = None

    try:
        # CHAMADA DA API - Usando Gemini 2.5 Flash (Equilíbrio de 2026)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            config=types.GenerateContentConfig(
                system_instruction=instrucao,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
            contents="Quais os 5 melhores notebooks custo-benefício IPS hoje no Brasil?"
        )

        # LIMPEZA DO JSON (Tratando textos extras da IA)
        texto_bruto = response.text
        # Pega tudo que estiver entre o primeiro { e o último }
        match = re.search(r'(\{.*\})', texto_bruto, re.DOTALL)
        
        if match:
            json_limpo = match.group(1)
            dados = json.loads(json_limpo)
            
            with open('ofertas.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            print("✅ SUCESSO! O gráfico de radar e os cards já podem ser visualizados.")
        else:
            print("❌ Erro: A IA não enviou os dados no formato esperado.")
            print("Resposta bruta:", texto_bruto)

    except Exception as e:
        print(f"❌ Falha na operação: {e}")
        if response:
            print("Conteúdo bruto recebido para análise técnica:", response.text)

if __name__ == "__main__":
    buscar_ofertas()