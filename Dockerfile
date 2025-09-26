# ====================
# Dockerfile - IUTESSA
# ====================

# Image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système utiles + Node.js + npm
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code Django
COPY . .

# ====================
# TAILWIND CSS
# ====================
# Installer dépendances Node dans theme/static_src
WORKDIR /app/theme/static_src
RUN npm install

# Construire Tailwind CSS
RUN npm run build

# ====================
# COLLECTSTATIC
# ====================
WORKDIR /app
RUN python manage.py collectstatic --noinput

# Exposer le port interne
EXPOSE 8000

# Lancer le serveur Uvicorn (ASGI)
CMD ["uvicorn", "iuttessa.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
