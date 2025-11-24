# Readme Timewise Api

🧠 TimeWise DL Productivity Coach API


API em FastAPI que analisa produtividade de usuários com atividades e scores diários, gerando insights e sugestões usando IA (OpenAI / ChatGPT).

🚀 Funcionalidades

- Recebe dados do usuário, atividades e scores diários.
- Gera análise de produtividade via modelo de IA.
- Retorna sugestões práticas para melhorar desempenho.
- Protegida por API Key (`x-api-key`) para segurança.

⚙️ Variáveis de Ambiente

Antes de rodar ou deployar a aplicação, configure:

```
DL_API_KEY=<sua_api_key_para_API>
OPENAI_API_KEY=<sua_api_key_OpenAI>
PORT=10000
```

No Render, configure essas variáveis através do painel Environment da sua aplicação.

🐍 Rodando Localmente

Clone o repositório:

```
git clone https://github.com/seu-usuario/TimeWise-DeepLearning.git
cd TimeWise-DeepLearning/dl-api/app
```

Crie um ambiente virtual e instale dependências:

```
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Rode a API:

```
uvicorn main:app --reload --port 10000
```

📡 Endpoint Principal

`POST /v1/analise-produtividade`

Headers:

```
x-api-key: <DL_API_KEY>
Content-Type: application/json
```

Body Exemplo:

```json
{
  "usuario": {"id":1,"nome":"Ana","email":"ana@email.com"},
  "atividades": [{"nome":"Reunião","tipo":"trabalho","tempoInicio":"2025-11-23T09:00:00","tempoFim":"2025-11-23T10:00:00"}],
  "scores": [{"dataTrabalho":"2025-11-23","valor":8}],
  "modo":"chat"
}
```

Resposta Exemplo:

```json
{
  "status":"ok",
  "analise":"Produtividade boa, mas pode melhorar o foco...",
  "sugestoes":[{"titulo":"Priorize tarefas importantes","descricao":"Foque nas tarefas que geram mais impacto."}],
  "meta":{"model":"gpt-4","latency_ms":120}
}
```

🐳 Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dl-api/app/ .
EXPOSE 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```

☁️ Deploy no Render

`render.yaml`:

```yaml
services:
  - type: web
    name: timewise-ai-api
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DL_API_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
```

Testando a API no Render:

Copie o URL público gerado pelo Render, exemplo:

```
https://timewise-ai-api.onrender.com
```

Use ferramentas como Postman ou Insomnia para fazer o POST:

URL: `https://timewise-ai-api.onrender.com/v1/analise-produtividade`

Headers: `x-api-key: <DL_API_KEY>`

Body: JSON conforme exemplo acima.

✅ Observações

- API Key é obrigatória para acesso.
- `scores.valor` deve ser inteiro entre 0 e 10.
- `atividades.tempoInicio` e `atividades.tempoFim` devem estar no formato ISO 8601.

📄 Licença

MIT License
