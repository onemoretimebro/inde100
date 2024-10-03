import streamlit as st
import requests
import time


# URL de l'API Flask
FLASK_SERVER_URL = "indecence.ddns.net:5000/upload"  # Remplace par ton IP publique ou ton domaine DynDNS

st.title("Capture d'image avec caméra arrière et envoi au serveur Flask")

# Fonction JavaScript pour récupérer la géolocalisation du navigateur
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            document.dispatchEvent(new CustomEvent("geolocation_received", {detail: coords}));
        },
        (error) => {
            document.dispatchEvent(new CustomEvent("geolocation_error", {detail: error.message}));
        });
    </script>
""", unsafe_allow_html=True)

# Récupération de la géolocalisation envoyée par JavaScript
loc = st.experimental_get_query_params()

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
            # Vérifier si la localisation est récupérée via JavaScript
            if loc:
                lat = loc.get("latitude", ["Non disponible"])[0]
                lon = loc.get("longitude", ["Non disponible"])[0]
            else:
                st.warning("La localisation n'a pas été autorisée ou n'est pas disponible.")
                lat, lon = "Non disponible", "Non disponible"

            # Préparer les données pour l'envoi
            files = {"file": image.getvalue()}
            data = {"latitude": lat, "longitude": lon}

            # Envoi de l'image au serveur Flask
            response = requests.post(FLASK_SERVER_URL, files=files, data=data)
            if response.status_code == 200:
                st.write(f"Réponse du serveur : {response.json()}")
            else:
                st.error("Erreur lors de l'envoi de l'image au serveur.")

        # Attendre 3 secondes avant la prochaine capture
        time.sleep(3)

