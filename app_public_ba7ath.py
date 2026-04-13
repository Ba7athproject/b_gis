"""
Ba7ath GIS - PLATEFORME D'INVESTIGATION ENVIRONNEMENTALE
-------------------------------------------------------
Projet : Ba7ath (Vulgarisation OSINT - Monde Arabe/Tunisie)
Rôle : Dashboard public unifié pour enquêtes de démonstration.
Déploiement : Identité visuelle, Sélecteur de couches, Briefing complet.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os

# ==========================================
# 1. CONFIGURATION & IDENTITÉ VISUELLE
# ==========================================
st.set_page_config(
    page_title="Ba7ath GIS - Intelligence Environnementale",
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour renforcer l'identité Ba7ath
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; border-left: 5px solid #d35400; }
    .stExpander { background-color: #f8f9fa; border-radius: 5px; }
    h1 { color: #2c3e50; font-weight: 800; }
    .sidebar-footer { font-size: 11px; color: #7f8c8d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DISCLAIMER & PRÉSENTATION
# ==========================================
st.title("🌍 Ba7ath GIS : Archives & Enquêtes Satellitaires")

# Rappel crucial du cadre du projet
st.info("""
**📌 Note de Démonstration :** Cette plateforme présente des données récoltées dans le cadre d'un projet d'enquête plus vaste mené par **Ba7ath**. 
Il s'agit d'une preuve de concept (PoC) utilisant des données réelles pour démontrer l'efficacité des méthodologies OSINT dans la documentation des crises climatiques en Tunisie.
""")

# BRIEFING MÉTHODOLOGIQUE COMPLET (Restauré)
with st.expander("🔍 BRIEFING MÉTHODOLOGIQUE & SOURCES (À consulter avant analyse)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📡 Sources des Données
        * **Sentinel-2 (Optique) :** Analyse du couvert végétal via le capteur multi-spectral (Résolution 10m).
        * **Sentinel-1 (Radar SAR) :** Détection de l'eau par analyse de la rétrodiffusion micro-ondes (Capacité de vision à travers les nuages).
        * **JRC Global Surface Water :** Données de référence de la Commission Européenne pour l'eau permanente.
        * **FAO GAUL :** Limites administratives des gouvernorats tunisiens.
        """)
    with col2:
        st.markdown("""
        ### 🛠️ Définitions Techniques
        * **NDVI (Indice Végétation) :** Mesure de la photosynthèse. Une baisse de cet indice sur plusieurs années indique une dégradation des sols ou une désertification.
        * **SAR (Synthetic Aperture Radar) :** Technologie permettant de "voir" les inondations même sous une tempête grâce aux ondes radar.
        * **Zones de Dégradation :** Surfaces ayant perdu plus de 15% de leur biomasse par rapport à la période de référence.
        """)
    st.markdown("---")
    st.warning("⚠️ **Limites :** L'analyse radar peut être perturbée en zone urbaine dense. Les inondations éclair (Flash Floods) très brèves peuvent ne pas être capturées selon le cycle de passage du satellite.")

# ==========================================
# 3. BARRE LATÉRALE (LOGO & CATALOGUE)
# ==========================================
# Gestion du Logo Ba7ath
LOGO_PATH = "assets/logo_ba7ath.png"
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='text-align: center; color: #d35400;'>Ba7ath GIS</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("📂 Catalogue d'enquêtes")

# Catalogue détaillé
ENQUETES = {
    "🌊 Inondations : Nabeul (Janvier 2026)": {
        "type": "inondation",
        "file": "data/inondations_nabeul_2026.geojson",
        "center": [36.45, 10.73],
        "zoom": 11,
        "desc": "Analyse de la crue exceptionnelle de Janvier 2026. Comparaison radar avec la baseline historique."
    },
    "🏜️ Désertification : Kairouan (2019 vs 2025)": {
        "type": "desertification",
        "file": "data/desertification_kairouan_2019_2025.geojson",
        "center": [35.67, 10.10],
        "zoom": 10,
        "desc": "Suivi pluri-annuel du recul de la végétation. Focus sur les zones de dégradation critique."
    }
}

selected_event = st.sidebar.selectbox("Sélectionnez un dossier d'investigation :", list(ENQUETES.keys()))
event_data = ENQUETES[selected_event]

st.sidebar.markdown("---")
st.sidebar.write(f"**Focus de l'enquête :** {event_data['desc']}")

# Footer Branding
st.sidebar.markdown("<br><br><br><div class='sidebar-footer'>© 2026 Projet Ba7ath<br>Journalisme d'Investigation & Data-OSINT</div>", unsafe_allow_html=True)

# ==========================================
# 4. LOGIQUE VISUELLE & LÉGENDES RICHES
# ==========================================
def get_detailed_assets(etype):
    """Restitue les styles et les légendes techniques complètes."""
    if etype == "inondation":
        style = {'fillColor': '#d63031', 'color': '#c0392b', 'weight': 1, 'fillOpacity': 0.6}
        legend_html = """
        <div style="padding: 12px; background-color: #ffffff; border-radius: 5px; border: 1px solid #bdc3c7; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <strong style="color:#2c3e50;">📊 Légende Inondations (SAR)</strong><br>
            <div style="margin-top:8px;">
                <span style='color:#0984e3; font-size:18px;'>●</span> <b>Points de référence :</b> Eaux permanentes (Baseline JRC).<br>
                <span style='color:#d63031; font-size:18px;'>●</span> <b>Zones de Crise :</b> Eaux détectées en Janvier 2026 hors lits habituels.<br>
            </div>
            <small style="color:#7f8c8d;"><i>Note : Le radar détecte l'absence de signal sur les surfaces lisses.</i></small>
        </div>
        """
        return style, legend_html
    
    elif etype == "desertification":
        style = {'fillColor': '#e67e22', 'color': '#d35400', 'weight': 1, 'fillOpacity': 0.7}
        legend_html = """
        <div style="padding: 12px; background-color: #ffffff; border-radius: 5px; border: 1px solid #bdc3c7; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <strong style="color:#2c3e50;">📊 Échelle de Dégradation (NDVI)</strong><br>
            <div style="margin-top:8px; margin-bottom:5px;">Perte de vitalité végétale (2019-2025) :</div>
            <div style="width: 100%; height: 15px; background: linear-gradient(to right, #fee08b, #e67e22, #d35400, #3e1900); border: 1px solid #999;"></div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color:#555;">
                <span>Modérée</span>
                <span>Sévère</span>
                <span>Extrême</span>
            </div>
            <p style="font-size: 11px; margin-top:10px; color:#7f8c8d;"><i>Données traitées à 100m de résolution pour isoler les tendances de fond.</i></p>
        </div>
        """
        return style, legend_html
    return {'color': 'black'}, ""

# ==========================================
# 5. RENDU DE LA CARTE AVEC LAYER CONTROL
# ==========================================
st.subheader(f"📍 {selected_event}")

if os.path.exists(event_data["file"]):
    style_config, legend_code = get_detailed_assets(event_data["type"])
    
    # Création de la carte (tiles=None pour forcer le choix)
    m = folium.Map(location=event_data["center"], zoom_start=event_data["zoom"], control_scale=True, tiles=None)
    
    # Restauration des Fonds de Carte (Layers)
    folium.TileLayer('openstreetmap', name='Plan Urbain (OSM)').add_to(m)
    folium.TileLayer('cartodbpositron', name='Fond Clair (Épuré)').add_to(m)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
        attr='Google', 
        name='Vue Satellite Hybride',
        overlay=False
    ).add_to(m)

    # Chargement GeoJSON
    with open(event_data["file"], 'r', encoding='utf-8') as f:
        geo_json_data = json.load(f)

    folium.GeoJson(
        geo_json_data, 
        name=f"Analyse Ba7ath : {selected_event}", 
        style_function=lambda x: style_config
    ).add_to(m)
    
    # CONTRÔLE DES COUCHES (Restauré)
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    # Affichage Map
    st_folium(m, height=650, use_container_width=True, returned_objects=[])

    # Affichage Légende Technique
    st.markdown(legend_code, unsafe_allow_html=True)

else:
    st.error(f"❌ Données manquantes : Le fichier `{event_data['file']}` n'a pas été trouvé dans le dossier /data.")
    st.info("💡 Exécutez le script d'extraction correspondant pour générer les données de cette enquête.")