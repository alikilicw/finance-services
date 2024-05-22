# Python resmi imajından başlayın
FROM python:3.9-slim

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
