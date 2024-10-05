import streamlit as st
import socketio

# Configuration du client SocketIO
sio = socketio.Client()

@sio.event
def connect():
    st.write("Connecté au serveur!")

@sio.event
def keyword_detected(data):
    st.write(f"Mot-clé détecté : {data['message']}")

@sio.event
def location_update(data):
    st.write(f"Nouvelle localisation reçue : {data['latitude']}, {data['longitude']}")

# Connexion au serveur SocketIO (ajuster l'URL selon votre configuration No-IP)
sio.connect('http://monapp.no-ip.org:8501')

# Interface Streamlit
st.title("Application de Reconnaissance Vocale et Géolocalisation")
st.write("Cliquez sur le bouton ci-dessous pour activer la reconnaissance vocale et la géolocalisation.")

# Zone pour afficher le texte reconnu en temps réel
recognized_text = st.empty()

# Bouton pour démarrer/arrêter la reconnaissance vocale
if st.button("Démarrer la reconnaissance vocale"):
    sio.emit('toggle_recognition')

# Injection du script JavaScript pour la reconnaissance vocale et la géolocalisation
st.markdown("""
    <script>
        const socket = io.connect('http://monapp.no-ip.org:8501');  // Modifier avec l'adresse No-IP si besoin
        let recognitionActive = false;
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'fr-FR';
        recognition.continuous = true;
        recognition.interimResults = false;

        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
            console.log("Reconnaissance : " + transcript);

            // Mettre à jour le texte reconnu en temps réel
            document.getElementById("recognized_text").textContent = transcript;

            if (transcript.includes("les poulets")) {
                console.log("Mot-clé détecté !");
                // Envoyer au serveur lorsque le mot-clé est détecté
                socket.emit('keyword_detected', { message: "Le mot-clé a été détecté !" });
            }
        };

        recognition.onerror = function(event) {
            console.error("Erreur de reconnaissance vocale : ", event.error);
            alert("Erreur de reconnaissance vocale : " + event.error);
        };

        recognition.onend = function() {
            if (recognitionActive) {
                recognition.start();
            }
        };

        // Fonction pour démarrer/arrêter la reconnaissance vocale
        function toggleRecognition() {
            if (recognitionActive) {
                recognition.stop();
                document.getElementById("toggle_button").textContent = "Démarrer la reconnaissance vocale";
            } else {
                recognition.start();
                document.getElementById("toggle_button").textContent = "Arrêter la reconnaissance vocale";
            }
            recognitionActive = !recognitionActive;
        }

        // Fonction pour obtenir la localisation
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, handleError, {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                });
            } else {
                console.error("La géolocalisation n'est pas supportée par ce navigateur.");
            }
        }

        function showPosition(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            console.log("Latitude : " + latitude + ", Longitude : " + longitude);
            socket.emit('location_update', { latitude: latitude, longitude: longitude });
        }

        function handleError(error) {
            console.error("Erreur de géolocalisation : ", error);
        }

        // Demander l'accès au microphone et à la géolocalisation dès le chargement de la page
        window.onload = function() {
            toggleRecognition();  // Démarre la reconnaissance vocale

            // Demande d'accès à la géolocalisation
            getLocation();

            // Mise à jour de la localisation toutes les 5 secondes
            setInterval(getLocation, 5000);
        };
    </script>

    <div>
        <strong>Texte reconnu :</strong> <span id="recognized_text">En attente de la reconnaissance...</span>
    </div>
    <button id="toggle_button" onclick="toggleRecognition()">Démarrer la reconnaissance vocale</button>
    """, unsafe_allow_html=True)
