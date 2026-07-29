from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from config import EMBEDDING_MODEL, DB_DIRECTORY

def get_qa_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # Görev adını güncel sürümle uyumlu olacak şekilde 'text-generation' yaptık
    hf_pipeline = pipeline("text-generation", model="google/flan-t5-small", max_new_tokens=256)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    return retriever, llm