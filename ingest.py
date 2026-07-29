import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import EMBEDDING_MODEL, DB_DIRECTORY, DOCUMENTS_DIRECTORY

def ingest_documents():
    if not os.path.exists(DOCUMENTS_DIRECTORY):
        os.makedirs(DOCUMENTS_DIRECTORY)
    
    # Türkçe karakter ve encoding sorununu önlemek için loader_kwargs eklendi
    loader = DirectoryLoader(
        DOCUMENTS_DIRECTORY, 
        glob="./*.txt", 
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )
    print("Film verileri başarıyla işlendi ve yerel veritabanına kaydedildi!")

if __name__ == "__main__":
    ingest_documents()