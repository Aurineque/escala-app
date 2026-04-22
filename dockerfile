# Usa uma versão leve do Python
FROM python:3.12-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia a lista de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código para dentro do container
COPY . .

# Expõe a porta que vamos usar
EXPOSE 8080

# O comando mágico para ligar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]