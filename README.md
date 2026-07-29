# 🎬 Seçici İzleyici | Yerel Film & Dizi RAG Asistanı

> Microsoft Summer Internship 2026 — *Building Your First Local RAG Application with Foundry Local*

Tamamen **lokalde** çalışan, cloud bağlantısı gerektirmeyen, özel bir veri setine dayalı RAG (Retrieval-Augmented Generation) asistanı. Film ve dizi verilerini bilgi tabanı olarak kullanır; interaktif, rehberli arayüzü ve akıllı filtreleme mantığıyla kullanıcılara en uygun yapımları önerir.

---

## 🏗️ Mimari
Kullanıcı Tercihleri / Sorusu
│
▼
[Streamlit UI (Adım Adım Sihirbaz & Kart Görünümü)]
│
▼
[Sentence Transformers - HuggingFace Embeddings]
│
▼
[ChromaDB - Yerel Vektör Benzerlik Araması] → Top-3 Belge
│
▼
[Yerel Dil Modeli / Veri Eşleştirme Katmanı]
│
▼
Özelleştirilmiş Film / Dizi Önerisi
## 🛠️ Tech Stack

| Bileşen | Araç |
|---|---|
| LLM / Veri İşleme | Transformers & LangChain |
| Vector Database | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) |
| UI | Streamlit (Özel CSS & Kart Yapısı) |
| Data | Özel Film & Dizi Veri Seti (`documents/`) |
| Language | Python 3.11+ |

---

## 🚀 Kurulum

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/kullanici-adin/repo-adin.git](https://github.com/kullanici-adin/repo-adin.git)
cd repo-adin