FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/.gitkeep ./data/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV INVENTARIO_JSON_PATH=/app/data/inventario.json

ENTRYPOINT ["./entrypoint.sh"]
