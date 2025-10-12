# ===============================
# Base image
# ===============================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ===============================
# Dépendances système
# ===============================
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Dépendances Python
# ===============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Copier le code source
# ===============================
COPY . .

# ===============================
# Créer les dossiers nécessaires
# ===============================
RUN mkdir -p \
    /app/media/blog/featured \
    /app/media/blog/images \
    /app/media/blog/gallery \
    /app/media/blog/videos \
    /app/media/blog/documents \
    /app/media/portfolio/images \
    /app/media/events \
    /app/media/courses \
    /app/staticfiles/css/dist

# ===============================
# Permissions
# ===============================
RUN chown -R www-data:www-data /app/media /app/staticfiles

# ===============================
# Build Tailwind directement dans staticfiles
# ===============================
WORKDIR /app/theme/static_src
RUN npm install
RUN npx tailwindcss -i ./src/styles.css -o ../../staticfiles/css/dist/styles.css --minify

# ===============================
# Collectstatic pour s'assurer que tout est dans /staticfiles
# ===============================
WORKDIR /app
RUN python manage.py collectstatic --noinput

# ===============================
# Passer à l'utilisateur www-data
# ===============================
USER www-data

EXPOSE 8000

# ===============================
# Commande de lancement
# ===============================
CMD ["uvicorn", "iuttessa.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
