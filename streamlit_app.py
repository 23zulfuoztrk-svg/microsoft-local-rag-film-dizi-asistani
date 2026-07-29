import os
import streamlit as st

# Sayfa yapılandırması
st.set_page_config(
    page_title="Seçici İzleyici | Film & Dizi Asistanı",
    page_icon="🎬",
    layout="centered",
)

# --- ŞIK VE TEMİZ ÖZEL CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f1014;
        color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    .chat-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(180deg, rgba(229, 9, 20, 0.2) 0%, rgba(15, 16, 20, 0) 100%);
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #262730;
    }
    .chat-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .chat-title span {
        color: #e50914;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Başlık
st.markdown(
    """
    <div class="chat-header">
        <p class="chat-title">Seçici <span>İzleyici Asistanı</span></p>
        <p style="color: #9ca3af; margin: 0;">3 adımda sana en uygun yapımı bulalım</p>
    </div>
""",
    unsafe_allow_html=True,
)


# --- VERİ SETİNİ OKUMA FONKSİYONU ---
def veri_setini_yukle():
  dosya_yolu = "documents/filmler diziler.txt"
  if not os.path.exists(dosya_yolu):
    return []

  with open(dosya_yolu, "r", encoding="utf-8") as f:
    icerik = f.read()

  bloklar = icerik.split("=== İÇERİK")
  arsiv = []

  for blok in bloklar:
    if not blok.strip():
      continue
    satirlar = blok.strip().split("\n")
    veri = {}
    for satir in satirlar:
      if ":" in satir:
        anahtar, deger = satir.split(":", 1)
        veri[anahtar.strip()] = deger.strip()

    if "Ad" in veri:
      arsiv.append({
          "ad": veri.get("Ad", ""),
          "medya_tipi": veri.get("Medya Tipi", ""),
          "mensei": veri.get("Menşei", ""),
          "tur": veri.get("Tür", ""),
          "imdb": veri.get("IMDb Puanı", ""),
          "oyuncular": veri.get("Oyuncular", ""),
          "konu": veri.get("Konu Detayı", ""),
          "gorsel": veri.get("Görsel", ""),
      })
  return arsiv


# Oturum Durumu Tanımlamaları
if "messages" not in st.session_state:
  st.session_state.messages = [
      {
          "role": "assistant",
          "content": (
              "Merhaba! Ben Seçici İzleyici Asistanı'yım. 🎬 Sana en kusursuz"
              " öneriyi yapabilmem için adım adım ilerleyelim.\n\n**1. Soru:**"
              " Bugün ne izlemek istersin?"
          ),
      }
  ]

if "asama" not in st.session_state:
  st.session_state.asama = "medya_secimi"
if "secilen_medya" not in st.session_state:
  st.session_state.secilen_medya = None
if "secilen_mensei" not in st.session_state:
  st.session_state.secilen_mensei = None

# Sohbet Geçmişini Ekrana Yazdırma
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# --- 1. AŞAMA: Film mi Dizi mi? ---
if st.session_state.asama == "medya_secimi":
  col1, col2 = st.columns(2)
  with col1:
    if st.button("📽️ Film", use_container_width=True):
      st.session_state.secilen_medya = "Film"
      st.session_state.messages.append(
          {"role": "user", "content": "Film izlemek istiyorum."}
      )
      st.session_state.messages.append({
          "role": "assistant",
          "content": (
              "Harika bir film seçildi! 📽️\n\n**2. Soru:** Hangi menşei"
              " tercih edersin? (Örn: Hollywood / Yabancı, Türk Yapımı vb.)"
          ),
      })
      st.session_state.asama = "mensei_secimi"
      st.rerun()

  with col2:
    if st.button("📺 Dizi", use_container_width=True):
      st.session_state.secilen_medya = "Dizi"
      st.session_state.messages.append(
          {"role": "user", "content": "Dizi izlemek istiyorum."}
      )
      st.session_state.messages.append({
          "role": "assistant",
          "content": (
              "Soluksuz izlenecek diziler seçildi! 📺\n\n**2. Soru:** Hangi"
              " menşei tercih edersin? (Örn: K-Drama (Kore Dizileri), Hollywood"
              " / Yabancı, Türk Dizileri vb.)"
          ),
      })
      st.session_state.asama = "mensei_secimi"
      st.rerun()

# --- 2. AŞAMA: Menşei / Köken Seçimi ---
elif st.session_state.asama == "mensei_secimi":
  if user_prompt := st.chat_input("Menşei/Köken belirtin..."):
    st.session_state.secilen_mensei = user_prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
      st.markdown(user_prompt)

    asistan_yaniti = (
        f"Anlaşıldı ({user_prompt}).\n\n**3. Soru:** Ne tarz bir şeyler"
        " izlemek istiyorsun? (Örn: Aksiyon & Macera, Dram, Bilim Kurgu &"
        " Fantastik, Suç & Gizem, Korku & Gerilim, Komedi & Sitkom,"
        " Romantik)"
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": asistan_yaniti}
    )
    st.session_state.asama = "tur_secimi"
    st.rerun()

# --- 3. AŞAMA: Tür Seçimi, Esnek Filtreleme ve Kartlar ---
elif st.session_state.asama == "tur_secimi":
  if user_prompt := st.chat_input("İzlemek istediğiniz türü yazın..."):
    secilen_tur = user_prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
      st.markdown(user_prompt)

    tum_arsiv = veri_setini_yukle()

    girilen_mensei_terimleri = (
        st.session_state.secilen_mensei.lower().replace("-", "").split()
    )
    girilen_tur_terimleri = secilen_tur.lower().replace("-", "").split()

    filtrelenmis = []
    for item in tum_arsiv:
      item_tipi = item["medya_tipi"].lower()
      item_mensei = item["mensei"].lower().replace("-", "")
      item_tur = item["tur"].lower().replace("-", "")

      tip_uyusuyor = st.session_state.secilen_medya.lower() in item_tipi
      mensei_uyusuyor = any(
          terim in item_mensei for terim in girilen_mensei_terimleri
      )
      tur_uyusuyor = any(terim in item_tur for terim in girilen_tur_terimleri)

      if tip_uyusuyor and mensei_uyusuyor and tur_uyusuyor:
        filtrelenmis.append(item)

    with st.chat_message("assistant"):
      if filtrelenmis:
        baslik_mesaji = f"🎉 Kriterlerine uygun **{len(filtrelenmis)}** yapım bulundu:"
        st.markdown(baslik_mesaji)

        birlesmis_icerik = baslik_mesaji + "\n\n"

        for film in filtrelenmis:
          with st.container(border=True):
            col_img, col_txt = st.columns([1, 2])

            with col_img:
              if film["gorsel"]:
                try:
                  st.image(film["gorsel"])
                except Exception:
                  st.info("🖼️ Görsel yüklenemedi")

            with col_txt:
              st.subheader(f"🎬 {film['ad']}")
              st.markdown(
                  f"**⭐ IMDb Puanı:** {film['imdb']} &nbsp;&nbsp;|&nbsp;&nbsp;"
                  f" **🏷️ Tür:** {film['tur']}"
              )
              st.markdown(f"**👥 Oyuncular:** {film['oyuncular']}")
              st.markdown(f"**📖 Konu Detayı:** {film['konu']}")

          birlesmis_icerik += (
              f"\n### 🎬 {film['ad']}\n- **IMDb:** {film['imdb']}\n- **Tür:**"
              f" {film['tur']}\n- **Oyuncular:**"
              f" {film['oyuncular']}\n- **Konu:** {film['konu']}\n"
          )

        st.session_state.messages.append(
            {"role": "assistant", "content": birlesmis_icerik}
        )
      else:
        uyari_mesaji = "Üzgünüm, bu kriterlere tam uyan bir içerik bulamadım. Farklı bir menşei veya tür deneyebilirsin."
        st.warning(uyari_mesaji)
        st.session_state.messages.append(
            {"role": "assistant", "content": uyari_mesaji}
        )

    st.session_state.asama = "bitti"
    st.rerun()

# --- BİTTİ / YENİDEN BAŞLAT ---
elif st.session_state.asama == "bitti":
  if st.button("🔄 Yeni Bir Arama Başlat", use_container_width=True):
    st.session_state.clear()
    st.rerun()