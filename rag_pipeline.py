import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline # veya Foundry/Lokal entegrasyonuna uygun LLM sınıfı
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Konfigürasyon ve Yol Ayarları
DB_DIRECTORY = "db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Eğer Microsoft Foundry / yerel model yolunu kullanıyorsan burayı güncelleyebilirsin
LOCAL_MODEL_NAME = "microsoft/Phi-4-mini-instruct" # Örnek model adı

def get_vectorstore():
    """ChromaDB vektör veritabanını yükler ve döndürür."""
    if not os.path.exists(DB_DIRECTORY):
        raise FileNotFoundError(f"'{DB_DIRECTORY}' dizini bulunamadı! Önce ingest.py dosyasını çalıştırmalısınız.")
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings)
    return vectorstore

def create_rag_chain():
    """RAG (Retrieval-Augmented Generation) zincirini kurar."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3} # En benzer 3 belgeyi getirir
    )
    
    return retriever

def query_rag(question: str):
    """Kullanıcı sorusunu alır, vektör tabanından bağlam arar ve yanıt üretir."""
    retriever = create_rag_chain()
    docs = retriever.get_relevant_documents(question)
    
    # Bağlamı birleştirme
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Şimdilik eşleşen kaynakları ve metinleri döndüren yapı
    return {
        "question": question,
        "context": context,
        "source_documents": docs
    }

if __name__ == "__main__":
    # Test amaçlı çalıştırma
    test_soru = "Inception filminin konusu nedir?"
    print(f"Soru: {test_soru}\n")
    sonuc = query_rag(test_soru)
    print("Bulunan Kaynaklar ve Bağlam:")
    print(sonuc["context"])