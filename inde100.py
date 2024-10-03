import streamlit as st
import requests
import time


# URL de l'API Flask
FLASK_SERVER_URL = "indecence.ddns.net:5000/upload"  # Remplace par ton IP publique ou ton domaine DynDNS

# Fonction pour capturer l'image
def capture_image():
    st.text("Demande d'accès à la caméra arrière...")
    image = st.camera_input("Prendre une photo avec la caméra arrière")

    if image:
        st.image(image, caption="Image capturée", use_column_width=True)
        return image
    else:
        return None

# Bouton pour capturer et envoyer l'image
if st.button('Capturer et envoyer l\'image'):
    image = capture_image()

    if image:
        # Récupérer la localisation via l'événement JavaScript
        lat = st.session_state.get("latitude", "Non disponible")
        lon = st.session_state.get("longitude", "Non disponible")

        # Préparer les données pour l'envoi
        files = {"file": image.getvalue()}
        data = {"latitude": lat, "longitude": lon}

        # Envoi de l'image au serveur Flask
        response = requests.post(FLASK_SERVER_URL, files=files, data=data)
        if response.status_code == 200:
            st.write(f"Réponse du serveur : {response.json()}")
        else:
            st.error("Erreur lors de l'envoi de l'image au serveur.")
