# Usa uma imagem oficial do Python, bem leve (alpine ou slim)
FROM python:3.9-slim

# Define o diretorio de trabalho dentro do conteiner
WORKDIR /app

# Copia apenas o arquivo de dependencias primeiro (otimizacao de cache do Docker)
COPY requirements.txt .

# Instala as dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do codigo da aplicacao para dentro do conteiner
COPY . .

# Expoe a porta 5000 para o mundo exterior
EXPOSE 5000

# Comando para rodar a aplicacao quando o conteiner iniciar
CMD ["python", "app.py"]
