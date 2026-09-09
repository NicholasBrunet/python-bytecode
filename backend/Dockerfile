FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY backend/src/ src/

EXPOSE 8080

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]

