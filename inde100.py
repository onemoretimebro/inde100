import streamlit as st
from streamlit_geolocation import streamlit_geolocation

# Fonction pour vérifier si le mot-clé est détecté
def check_keyword_and_capture_location(keyword):
    user_input = st.text_input("Tapez quelque chose :")
    if keyword in user_input.lower():
        location = streamlit_geolocation()
        if location:
            st.write(f"Localisation capturée : {location['latitude']}, {location['longitude']}")
        else:
            st.write("Impossible d'obtenir la localisation.")
    else:
        st.write("Le mot-clé n'a pas été détecté.")

# Titre de l'application
st.title("Application de géolocalisation")

# Vérification du mot-clé
check_keyword_and_capture_location("les poulets")
