# Usar imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivos de requisitos
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta dl-api/app para o container
COPY dl-api/app/ .

# Expõe a porta padrão do Render
EXPOSE 10000

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
