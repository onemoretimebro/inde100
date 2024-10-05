from flask import Flask, render_template
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Liste pour stocker les adresses
addresses = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Un utilisateur s'est connecté.")

@socketio.on('keyword_detected')
def handle_keyword_detected(data):
    print(f"Mot-clé détecté par un client : {data['message']}")
    
    latitude = data['latitude']
    longitude = data['longitude']
    
    # Conversion des coordonnées en adresse
    address = get_address(latitude, longitude)
    
    # Émettre l'adresse formatée à tous les clients connectés
    socketio.emit('notify_clients', {'address': address})


def get_address(latitude, longitude):
    try:
        headers = {
            'User-Agent': 'MonApplication/1.0 (http://mon-application.com)'  # Remplacez par votre URL
        }
        response = requests.get(
            f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json',
            headers=headers
        )

        print("Réponse brute de l'API:", response.text)  # Afficher la réponse brute

        if response.status_code == 200:
            data = response.json()
            print("Données de l'adresse :", data)  # Afficher les données JSON
            
            # Extraire les éléments souhaités
            address_parts = []
            
            # Ajout des parties de l'adresse spécifiques que vous souhaitez
            if 'house_number' in data['address']:
                address_parts.append(data['address']['house_number'])  # Numéro de la maison
            if 'road' in data['address']:
                address_parts.append(data['address']['road'])  # Rue
            if 'hamlet' in data['address']:
                address_parts.append(data['address']['hamlet'])  # Petit hameau
            if 'suburb' in data['address']:
                address_parts.append(data['address']['suburb'])  # Quartier

            # Vérification si des parties d'adresse ont été ajoutées
            print("Parties d'adresse extraites :", address_parts)
            
            # Construire l'adresse formatée
            formatted_address = ', '.join(address_parts)
            return formatted_address if formatted_address else "Adresse inconnue"
        else:
            print(f"Erreur HTTP : {response.status_code} - {response.text}")
            return "Erreur dans la récupération de l'adresse"
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse : {e}")
        return "Erreur dans la récupération de l'adresse"



@socketio.on('location_update')
def handle_location_update(data):
    print(f"Localisation reçue : Latitude {data['latitude']}, Longitude {data['longitude']}")

if __name__ == '__main__':
    # Flask écoute sur toutes les interfaces pour être accessible depuis d'autres appareils du réseau local
    socketio.run(app, debug=True)
