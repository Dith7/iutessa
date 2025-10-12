# ======================
# Dockerfile - IUTESSA
# ======================
FROM python:3.11-slim

# Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Installer Node.js + dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Installer dépendances JS pour Tailwind
WORKDIR /app/theme/static_src
RUN npm install

# Compiler Tailwind CSS
RUN npx tailwindcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify

# Revenir dans le dossier principal
WORKDIR /app

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Lancer le serveur
CMD ["uvicorn", "iuttessa.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
