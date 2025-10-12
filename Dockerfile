# Image de base Python
FROM python:3.11-slim

# Variables d'environnement de base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système + Node.js + npm
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@10 \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code Django
COPY . .

# Installer les dépendances Node et construire Tailwind
WORKDIR /app/theme/static_src

# Supprime les anciens node_modules s’ils existent
RUN rm -rf node_modules package-lock.json

# Installe Tailwind 3.x et PostCSS
RUN npm install -D tailwindcss@3.4.13 postcss autoprefixer cross-env && npm install

# Build Tailwind (sans Django Tailwind)
RUN npx tailwindcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify

# Revenir au répertoire principal
WORKDIR /app

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port interne
EXPOSE 8000

# Lancer avec Uvicorn
CMD ["uvicorn", "iuttessa.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
