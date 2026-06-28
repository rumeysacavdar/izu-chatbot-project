import requests
import io
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# Yeni eklenen linkleri içeren dosyayı oku
with open("yeni_eklenenler.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

os.makedirs("data/ders_programlari", exist_ok=True)

for i, url in enumerate(urls):
    try:
        response = requests.get(url)
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            pdf_file = io.BytesIO(response.content)
            reader = PdfReader(pdf_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ""
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cols = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
                    if cols: text += " | ".join(cols) + "\n"
            
            # Tablo yoksa düz metni de al (Erasmus/ÇAP sayfaları için)
            if not text:
                text = soup.get_text(separator="\n", strip=True)
        
        # GÜVENLİ İSİMLENDİRME: Ders programlarını bozmamak için 'ek_bilgi' adıyla kaydediyoruz
        with open(f"data/ders_programlari/ek_bilgi_{i}.txt", "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n{text}")
        print(f"İşlendi: ek_bilgi_{i}.txt")
    except Exception as e:
        print(f"Hata: {url} -> {e}")