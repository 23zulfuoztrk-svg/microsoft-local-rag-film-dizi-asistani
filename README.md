## 🤖 Microsoft Foundry Local ile Yerel RAG Film & Dizi Asistanı

> Microsoft Yaz Stajı 2026 — Foundry Local ile İlk Yerel RAG Uygulamanızı Oluşturma

Tamamen lokalde çalışan, bulut bağlantısı gerektirmeyen bir RAG (Retrieval-Augmented Generation) film ve dizi chatbotu. Yerel film/dizi bilgi tabanını kullanır ve Phi-4-mini model ile analizleri akıllı, kaynak destekli cevaplar verir.

---

## 🏗️ Mimari

```text
Kullanıcı Sorusu
  │
  ▼
[Streamlit UI]
  │
  ▼
[Sentence Transformers - Multilingual Embedding]
  │
  ▼
[ChromaDB - Vektör Benzerlik Araması] → Top-3 Belge
  │
  ▼
[Microsoft Foundry Local - Phi-4-mini]
  │
  ▼
Kaynaklı Cevap
```

## 🛠️ Tech Stack

| Bileşen | Araç |
|---|---|
| LLM Inference | Microsoft Foundry Local (Phi-4-mini) |
| Vector Database | ChromaDB |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 |
| UI | Streamlit |
| Data | Yerel Film & Dizi Metin Dosyası|
| Language | Python 3.11+ |

---

## 🚀 Kurulum

### 1. Foundry Local Kur
```winget install Microsoft.FoundryLocal
foundry model download phi-4-mini
```

### 2. Python Bağımlılıklarını Kur
```bash
pip install -r gereksinimler.txt
```

### 3. Bilgi Tabanını Oluştur
```bash
python ingest.py
```
> Wikipedia'dan ~20 Türkçe teknoloji makalesi indirir ve ChromaDB'ye yükler. (~2-3 dakika)

### 4. Chatbot'u Başlat
```bash
python -m streamlit run streamlit_app.pyy
```
> Tarayıcında `http://localhost:8501` adresinde açılır.

---

## 💡 Örnek Sorular

"Bana bilim kurgu filmi önerir misin?"

"Inception filminin konusu nedir?"

"Christopher Nolan filmleri nelerdir?"

"Dram türündeki en popüler diziler hangileridir?"

---

## 📁 Proje Yapısı

```
microsoft-local-rag-film-dizi-asistani/
├── app.py                # Streamlit chatbot arayüzü
├── rag_pipeline.py       # RAG mantığı (sorgu -> arama -> cevap)
├── ingest.py             # Veri yükleme ve indeksleme
├── config.py             # Model ve ayar konfigürasyonu
├── gereksinimler.txt     # Python bağımlılıkları
└── chroma_db/            # ChromaDB vektör veritabanı (gitignore)
```

---

## 🔒 Gizlilik & Güvenlik

- ✅ Tüm veriler ve işlemler yerel makinede kalır
- ✅ İnternet bağlantısı gerektirmez (kurulumdan sonra)
- ✅ API anahtarı veya bulut aboneliği gerekmez

---

## 📋 Gereksinimler

- Windows 10/11
- Python 3.11+
- 8 GB+ RAM (16 GB önerilir)
- NVIDIA GPU (önerilir) veya modern CPU
