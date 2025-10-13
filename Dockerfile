FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système (🔥 ajout de netcat-openbsd)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Créer dossiers media
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

# Permissions sur les dossiers media
RUN chmod -R 755 /app/media

# Tailwind
WORKDIR /app/theme/static_src
RUN npm install
RUN npx tailwindcss -i ./src/styles.css -o ../../staticfiles/css/dist/styles.css --minify

# Collectstatic
WORKDIR /app
RUN python manage.py collectstatic --noinput

# Copier entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]