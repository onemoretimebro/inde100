import streamlit as st
import requests
import time
from geopy.geocoders import Nominatim
from streamlit_javascript import st_javascript

# URL de l'API Flask
FLASK_SERVER_URL = "indecence.ddns.net:5000/upload"  # Remplace par ton IP publique ou ton domaine DynDNS

st.title("Capture d'image avec caméra arrière et envoi au serveur Flask")

# Obtenir la localisation de l'utilisateur
loc = geolocation()

# Fonction pour capturer l'image
def capture_image():
    st.text("Demande d'accès à la caméra arrière...")
    image = st.camera_input("Prendre une photo avec la caméra arrière")

    if image:
        st.image(image, caption="Image capturée", use_column_width=True)
        return image
    else:
        return None

# Bouton pour démarrer la capture automatique
if st.button('Commencer la capture automatique'):
    st.write("Capture et envoi des images toutes les 3 secondes...")
    while True:
        image = capture_image()
        if image:
            # Récupérer la localisation
            if loc:
                lat = loc['coords']['latitude']
                lon = loc['coords']['longitude']
            else:
                st.warning("La localisation n'a pas été autorisée ou n'est pas disponible.")
                lat, lon = None, None

            # Préparer les données pour l'envoi
            files = {"file": image.getvalue()}
            data = {}
            if lat and lon:
                data = {"latitude": lat, "longitude": lon}
            else:
                data = {"latitude": "Non disponible", "longitude": "Non disponible"}

            # Envoi de l'image au serveur Flask
            response = requests.post(FLASK_SERVER_URL, files=files, data=data)
            if response.status_code == 200:
                st.write(f"Réponse du serveur : {response.json()}")
            else:
                st.error("Erreur lors de l'envoi de l'image au serveur.")

        # Attendre 3 secondes avant la prochaine capture
        time.sleep(3)

