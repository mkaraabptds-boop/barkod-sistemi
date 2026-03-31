import streamlit as st
import cv2
import numpy as np
import zxingcpp
from PIL import Image

# --- PROFESYONEL ARAYÜZ ---
st.set_page_config(page_title="ABP TDS Akıllı Motor", layout="centered")
st.markdown("""
    <style>
    .stCamera { border: 5px solid #00ff00; border-radius: 15px; }
    .stButton>button { background-color: #00ff00; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ABP TDS - Akıllı Barkod Motoru")
st.write("Bu sistem sadece resim çekmez; pikselleri analiz ederek barkodu çözer.")

# --- KAMERA GİRİŞİ ---
img_file = st.camera_input("Barkodu Odaklayın ve Çekin")

if img_file:
    # 1. Ham Görüntüyü Al
    img = Image.open(img_file)
    img_array = np.array(img)
    
    # 2. DİJİTAL ANALİZ (Kamerayı Tarayıcıya Dönüştüren Kısım)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Filtre 1: Keskinleştirme (Çizgilerin kenarlarını belirginleştirir)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    
    # Filtre 2: Threshold (Gölgeyi siler, sadece siyah çizgileri bırakır)
    _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 3. OKUMA MOTORUNU ÇALIŞTIR
    st.info("Algoritma çalışıyor...")
    
    # Hem ham görüntüde hem de filtreli görüntülerde aynı anda ara
    results = []
    for target in [gray, binary, sharpened]:
        found = zxingcpp.read_barcodes(target)
        if found:
            results = found
            break

    if results:
        for result in results:
            # Code 39'daki yıldızları ve gereksiz boşlukları temizle
            clean_code = result.text.replace("*", "").strip()
            st.success(f"### 🎯 OKUNDU: {clean_code}")
            st.balloons()
    else:
        st.error("Yazılım çizgileri çözümleyemedi!")
        st.warning("Excel'de barkodun 'Boyunu' (yüksekliğini) uzatıp öyle fotoğraf çekmeyi dene kanka.")