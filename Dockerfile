FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Crear directorio de la app
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de arranque
CMD ["gunicorn", "vuelos_europa_api.api:app", "--bind", "0.0.0.0:8000"]
