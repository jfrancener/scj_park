# Imagem oficial Python slim (leve e otimizada)
FROM python:3.13-slim

# Evita que o Python grave arquivos .pyc no container
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que o Python faça buffer das saídas de log (mostra em tempo real)
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho interno
WORKDIR /app

# Instala ferramentas básicas necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . /app/

# Coleta os arquivos estáticos do Django (WhiteNoise)
RUN python manage.py collectstatic --noinput

# Expõe a porta interna da aplicação
EXPOSE 8000

# Executa migrações do banco SQLite e inicia o Gunicorn em produção
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 2 --bind 0.0.0.0:8000 park_project.wsgi:application"]
