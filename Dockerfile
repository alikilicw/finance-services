# Python resmi imajından başlayın
FROM python:3.12.3-bullseye

# Gerekli bağımlılıkları yükleyin
RUN apt-get update \
    && apt-get install -y firefox-esr \
    && apt-get install -y wget \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.30.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && apt-get clean

# Çalışma dizinini belirleyin
WORKDIR /app

# Gereksinim dosyasını (requirements.txt) çalışma dizinine kopyalayın
COPY requirements.txt .

# Gereksinimleri yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalayın
COPY . .

# Django uygulaması için gerekli ayarları ekleyin
EXPOSE 5002

# Django uygulamasını çalıştırın
CMD ["python", "manage.py", "runserver", "0.0.0.0:5002"]
