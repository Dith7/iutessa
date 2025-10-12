FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Créer dossiers media avec permissions
RUN mkdir -p /app/media/blog/featured \
    /app/media/blog/images \
    /app/media/blog/gallery \
    /app/media/blog/videos \
    /app/media/blog/documents \
    /app/media/portfolio/images \
    /app/media/events \
    /app/media/courses \
    /app/staticfiles \
    && chmod -R 777 /app/media \
    && chmod -R 755 /app/staticfiles

# Tailwind
WORKDIR /app/theme/static_src
RUN npm install
RUN npx tailwindcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify

WORKDIR /app
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uvicorn", "iuttessa.asgi:application", "--host", "0.0.0.0", "--port", "8000"]