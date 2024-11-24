FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=development \
    FLASK_DEBUG=1

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar a aplicação
COPY . .

# Criar diretório para o banco
RUN mkdir -p /app/data && chmod 777 /app/data

EXPOSE 5000

# Criar script de inicialização
RUN echo '#!/bin/bash\n\
python3 -c "from database import init_db; init_db()"\n\
python3 -m flask run --host=0.0.0.0 --port=5000' > /app/start.sh && \
    chmod +x /app/start.sh

# Usar o script de inicialização
CMD ["/app/start.sh"]