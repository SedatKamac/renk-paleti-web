import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from math import sqrt


color_meanings = {
    "red": "Tutku, enerji, cesaret, sevgi",
    "orange": "Canlılık, neşe, heyecan",
    "yellow": "Mutluluk, iyimserlik, yaratıcılık",
    "green": "Doğa, huzur, tazelik, denge",
    "blue": "Sakinlik, güven, sorumluluk",
    "purple": "Lüks, gizem, yaratıcılık",
    "pink": "Şefkat, aşk, sıcaklık",
    "brown": "Sağlamlık, doğallık, güven",
    "gray": "Nötr, denge, sakinlik",
    "black": "Güç, sofistike, gizem",
    "white": "Saflık, temizlik, basitlik"
}

def closest_color(rgb):
    colors_rgb = {
        "red": (255, 0, 0),
        "orange": (255, 165, 0),
        "yellow": (255, 255, 0),
        "green": (0, 128, 0),
        "blue": (0, 0, 255),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "brown": (165, 42, 42),
        "gray": (128, 128, 128),
        "black": (0, 0, 0),
        "white": (255, 255, 255)
    }
    
    min_dist = float('inf')
    closest = None
    for color_name, color_val in colors_rgb.items():
        dist = sqrt(sum((c1 - c2)**2 for c1, c2 in zip(rgb, color_val)))
        if dist < min_dist:
            min_dist = dist
            closest = color_name
    return closest

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def get_palette(image, k):
    image = image.resize((150, 150))
    pixels = np.array(image).reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = [rgb_to_hex(c) for c in colors]
    return colors, hex_colors

st.title("Resimden Renk Paleti Üretici")

uploaded_file = st.file_uploader("Bir resim yükleyin", type=["jpg", "jpeg", "png"])

num_colors = st.slider("Kaç renk çıkarılsın?", min_value=1, max_value=10, value=5)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Yüklenen Resim", use_column_width=True)

    colors, hex_colors = get_palette(image, num_colors)

    st.write("### Bulunan Renkler:")
    cols = st.columns(len(colors))

    for idx, col in enumerate(cols):
        with col:
            st.write(hex_colors[idx])
            st.markdown(
                f"<div style='background-color:{hex_colors[idx]}; width:100%; height:100px;'></div>",
                unsafe_allow_html=True,
            )
            
            
            rgb = colors[idx]
            
            main_color = closest_color(rgb)
            
            meaning = color_meanings.get(main_color, "Anlam bulunamadı")
            
            st.write(f"**Duygusal Anlam:** {meaning}")

