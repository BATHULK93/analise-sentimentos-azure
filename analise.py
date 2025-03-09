import requests
import json
import os

# Definir os dados do Azure AI (substitua com suas credenciais)
endpoint = os.getenv("AZURE_ENDPOINT", "https://seu-endpoint.cognitiveservices.azure.com/")
api_key = os.getenv("AZURE_API_KEY", "SUA_CHAVE_AQUI")
path = "/text/analytics/v3.1/sentiment"

# Criar diretório de inputs caso não exista
if not os.path.exists("inputs"):
    os.makedirs("inputs")

# Criar um arquivo de exemplo caso não exista
sentences_file = "inputs/sentencas.txt"
if not os.path.exists(sentences_file):
    with open(sentences_file, "w", encoding="utf-8") as f:
        f.write("Este produto é incrível! Estou muito satisfeito. 😍\\n")
        f.write("O atendimento foi péssimo, não recomendo. 😡\\n")
        f.write("O serviço foi bom, mas pode melhorar. 🤔\\n")

# Ler sentenças do arquivo
with open(sentences_file, "r", encoding="utf-8") as f:
    sentences = [{"id": str(i+1), "text": line.strip()} for i, line in enumerate(f.readlines())]

# Montar payload
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}
data = {"documents": sentences}

# Chamar API
response = requests.post(endpoint + path, headers=headers, data=json.dumps(data))
result = response.json()

# Exibir resultados
for doc in result.get("documents", []):
    print(f"Sentença: {sentences[int(doc['id']) - 1]['text']}")
    print(f"Sentimento: {doc['sentiment']}")
    print(f"Pontuações: {doc['confidenceScores']}\\n")
