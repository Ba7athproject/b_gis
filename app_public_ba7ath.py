"""
Ba7ath GIS - DASHBOARD PUBLIC FINAL (Déploiement)
Rôle : Affichage professionnel avec sélecteur de vue et identité visuelle.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os

# ==========================================
# 1. Configuration (Logo & Favicon)
# ==========================================
# Remplacez "🌍" par "assets/favicon.ico" si vous avez le fichier
st.set_page_config(
    page_title="Ba7ath GIS - OSINT Environmental Intelligence",
    page_icon="🌍", 
    layout="wide"
)

# Style CSS pour le branding
st.markdown("""
    <style>
    .stSidebar { background-color: #ffffff; border-right: 1px solid #e0e6ed; }
    h1 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Barre Latérale (Logo et Catalogue)
# ==========================================
LOGO_PATH = "assets/logo_ba7ath.png"
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='text-align: center; color: #d35400;'>Ba7ath GIS</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("📂 Catalogue d'enquêtes")

# Base de données des enquêtes
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
st.sidebar.markdown("<br><p style='font-size: 10px; color: #95a5a6;'>© 2026 Ba7ath Project</p>", unsafe_allow_html=True)

# ==========================================
# 3. Contenu Principal et Carte
# ==========================================
st.title(f"📍 {selected_name}")

with st.expander("📚 Méthodologie et Sources", expanded=False):
    st.markdown("""
    **Sources :** Copernicus Sentinel-1/2, JRC Global Surface Water.  
    **Méthode :** Analyse de changement (Change Detection) basée sur des données satellitaires réelles.
    """)

if os.path.exists(event["file"]):
    # Définition des styles
    if event["type"] == "inondation":
        style = {'fillColor': '#d63031', 'color': '#c0392b', 'weight': 1, 'fillOpacity': 0.6}
        legend_label = "Zones Inondées (SAR)"
    else:
        style = {'fillColor': '#e67e22', 'color': '#d35400', 'weight': 1, 'fillOpacity': 0.7}
        legend_label = "Dégradation NDVI"

    # INITIALISATION DE LA CARTE (tiles=None pour gérer nos propres fonds)
    m = folium.Map(location=event["center"], zoom_start=event["zoom"], control_scale=True, tiles=None)
    
    # AJOUT DES FONDS DE CARTE (Basemaps)
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(m)
    folium.TileLayer('cartodbpositron', name='Plan Clair (Street Map)').add_to(m)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
        attr='Google', 
        name='Vue Satellite (Hybride)',
        overlay=False
    ).add_to(m)

    # CHARGEMENT DU GEOJSON
    with open(event["file"], 'r', encoding='utf-8') as f:
        data = json.load(f)

    folium.GeoJson(data, name=legend_label, style_function=lambda x: style).add_to(m)
    
    # RÉACTIVATION DU CONTRÔLE DES COUCHES (Le sélecteur de vue)
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    # RENDU
    st_folium(m, height=650, use_container_width=True, returned_objects=[])

    # Légende visuelle
    if event["type"] == "inondation":
        st.markdown("<div style='padding:10px; border-left:5px solid #d63031; background:#f9f9f9;'>🟥 <b>Rouge :</b> Anomalie hydrique détectée par radar.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='padding:10px; border-left:5px solid #e67e22; background:#f9f9f9;'>🟧 <b>Orange :</b> Perte de couverture végétale significative.</div>", unsafe_allow_html=True)
else:
    st.error(f"Fichier introuvable : {event['file']}")