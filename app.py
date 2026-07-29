import streamlit as st
from rag_pipeline import query_rag

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Film & Dizi RAG Asistanı",
    page_icon="🎬",
    layout="centered"
)

# Arayüz Başlığı
st.title("🎬 Film & Dizi RAG Asistanı")
st.markdown("Tamamen yerelde çalışan, veri tabanındaki film ve dizilere göre kaynaklı cevaplar veren akıllı asistan.")

# Sohbet Geçmişini Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş Mesajları Ekrana Yazdırma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Girdi Alma
if prompt := st.chat_input("Film veya diziler hakkında ne öğrenmek istiyorsun?"):
    # Kullanıcı mesajını ekrana ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistanın Yanıt Üretmesi
    with st.chat_message("assistant"):
        with st.spinner("Bilgi tabanı aranıyor ve yanıt hazırlanıyor..."):
            try:
                # rag_pipeline üzerinden veriyi çek
                result = query_rag(prompt)
                context = result["context"]
                
                # Yanıt oluşturma mantığı (Burada model entegrasyonuna göre çıktı biçimlendirilebilir)
                if context:
                    response = f"**Bulunan İlgili Kaynaklar / Bağlam:**\n\n{context}"
                else:
                    response = "Üzgünüm, bilgi tabanımda bu soruyla ilgili yeterli veri bulamadım."
                
                st.markdown(response)
                
                # Asistan mesajını geçmişe kaydet
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_message = f"Bir hata oluştu: {str(e)}"
                st.error(error_message)