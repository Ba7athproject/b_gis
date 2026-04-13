"""
Ba7ath GIS - DASHBOARD PUBLIC FINAL
Déploiement : Logo, Favicon et Architecture Statique Professionnelle.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os

# ==========================================
# 1. Configuration (Logo & Favicon)
# ==========================================
# Note : Tu peux remplacer "🌍" par le chemin vers ton fichier : "assets/favicon.ico"
st.set_page_config(
    page_title="Ba7ath GIS - OSINT Environmental Intelligence",
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé pour le branding
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stSidebar { background-color: #ffffff; border-right: 1px solid #e0e6ed; }
    h1 { color: #2c3e50; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Barre Latérale (Logo et Navigation)
# ==========================================
# Affichage du Logo (Assure-toi que le fichier existe dans /assets)
LOGO_PATH = "assets/logo_ba7ath.png"
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    # Logo textuel de secours si l'image est absente
    st.sidebar.markdown("<h2 style='text-align: center; color: #d35400;'>Ba7ath GIS</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("📂 Catalogue d'enquêtes")

# ==========================================
# 3. Base de données des enquêtes
# ==========================================
ENQUETES = {
    "🌊 Inondations : Nabeul (Janvier 2026)": {
        "type": "inondation",
        "file": "data/inondations_nabeul_2026.geojson",
        "center": [36.45, 10.73],
        "zoom": 11,
        "desc": "Analyse radar (SAR) des crues de Janvier 2026 dans le Cap Bon."
    },
    "🏜️ Désertification : Kairouan (2019 vs 2025)": {
        "type": "desertification",
        "file": "data/desertification_kairouan_2019_2025.geojson",
        "center": [35.67, 10.10],
        "zoom": 10,
        "desc": "Indicateurs de dégradation sévère du couvert végétal en Tunisie Centrale."
    }
}

selected_name = st.sidebar.selectbox("Sélectionnez un dossier :", list(ENQUETES.keys()))
event = ENQUETES[selected_name]

st.sidebar.markdown("---")
st.sidebar.write(f"**Description :** {event['desc']}")

# Pied de page sidebar
st.sidebar.markdown("<br><br><br><p style='font-size: 10px; color: #95a5a6;'>© 2026 Ba7ath Project<br>OSINT Journalism & Environmental Intelligence</p>", unsafe_allow_html=True)

# ==========================================
# 4. Contenu Principal
# ==========================================
st.title(f"📍 {selected_name}")

# Briefing Méthodologique (Expander)
with st.expander("📚 Consulter la méthodologie et les sources", expanded=False):
    st.markdown("""
    **Sources :** Copernicus Sentinel-1/2, JRC Global Surface Water.
    **Méthode :** Les polygones affichés isolent les changements critiques par rapport aux données historiques de référence.
    **Limites :** Analyse basée sur une résolution spatiale de 50m à 100m.
    """)

# Logique de style et légendes
def get_assets(etype):
    if etype == "inondation":
        return {'fillColor': '#d63031', 'color': '#c0392b', 'weight': 1, 'fillOpacity': 0.6}, """
        <div style="padding: 10px; background-color: #ffffff; border-radius: 5px; border: 1px solid #d63031;">
            <span style='color:#d63031;'>⬤</span> <b>Zones Inondées :</b> Anomalie hydrique détectée par radar (SAR).
        </div>"""
    else:
        return {'fillColor': '#e67e22', 'color': '#d35400', 'weight': 1, 'fillOpacity': 0.7}, """
        <div style="padding: 10px; background-color: #ffffff; border-radius: 5px; border: 1px solid #e67e22;">
            <strong>Sévérité de la dégradation (NDVI)</strong><br>
            <div style="width: 100%; height: 12px; background: linear-gradient(to right, #fee08b, #e67e22, #3e1900); margin: 5px 0;"></div>
            <small>Modérée → Critique</small>
        </div>"""

# Affichage de la carte
if os.path.exists(event["file"]):
    style, legend = get_assets(event["type"])
    
    # Init Map
    m = folium.Map(location=event["center"], zoom_start=event["zoom"], control_scale=True)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                     attr='Google', name='Vue Satellite').add_to(m)

    # Load GeoJSON
    with open(event["file"], 'r', encoding='utf-8') as f:
        data = json.load(f)

    folium.GeoJson(data, name="Analyse Ba7ath", style_function=lambda x: style).add_to(m)
    
    # Rendu
    st_folium(m, height=600, use_container_width=True, returned_objects=[])
    st.markdown(legend, unsafe_allow_html=True)
else:
    st.error(f"Fichier de données manquant : {event['file']}")