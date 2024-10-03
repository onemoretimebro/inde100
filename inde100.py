import streamlit as st
import requests
import time
from geopy.geocoders import Nominatim

# URL de l'API Flask
FLASK_SERVER_URL = "indecence.ddns.net:5000/upload"  # Remplace par ton IP publique ou ton domaine DynDNS

st.title("Capture d'image avec caméra arrière et envoi au serveur Flask")

# Fonction pour capturer une image de la caméra arrière
def capture_image():
    st.text("Demande d'accès à la caméra arrière et à la localisation...")
    
    # Accès à la caméra arrière
    image = st.camera_input("Prendre une photo avec la caméra arrière")
    
    # Accès à la localisation
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode("Paris, France")  # Remplace par ta méthode de localisation réelle si nécessaire
    
    if image:
        # Affiche l'image
        st.image(image, caption="Image capturée", use_column_width=True)
        return image, location.latitude, location.longitude
    return None, None, None

# Boucle pour capturer l'image toutes les 3 secondes
while True:
    image, lat, lon = capture_image()
    if image:
        # Envoi de l'image au serveur Flask
        files = {"file": image.getvalue()}
        data = {"latitude": lat, "longitude": lon}
        
        response = requests.post(FLASK_SERVER_URL, files=files, data=data)
        st.write(response.text)
    
    # Attendre 3 secondes avant la prochaine capture
    time.sleep(3)

