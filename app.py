from rag_pipeline import get_qa_chain

def main():
    print("Seçici İzleyici Film/Dizi Asistanı Başlatıldı! (Çıkış için 'q' yazın)")
    retriever, llm = get_qa_chain()

    while True:
        query = input("\nKriterlerin nedir? (Örn: Uzay ve bilim kurgu seviyorum, ne izleyim?): ")
        if query.lower() == 'q':
            break
        
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = f"Bağlam:\n{context}\n\nSoru: {query}\n\nLütfen sadece yukarıdaki bağlama dayanarak öneride bulun:"
        response = llm.invoke(prompt)
        
        print("\nÖneri:", response)

if __name__ == "__main__":
    main()