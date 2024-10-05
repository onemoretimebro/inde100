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


def get_address(latitude, longitude, retry=0):
    try:
        headers = {
            'User-Agent': 'MonApplication/1.0 (http://mon-application.com)'  
        }
        response = requests.get(
            f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json',
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            address_parts = []
            if 'house_number' in data['address']:
                address_parts.append(data['address']['house_number'])
            if 'road' in data['address']:
                address_parts.append(data['address']['road'])
            if 'hamlet' in data['address']:
                address_parts.append(data['address']['hamlet'])
            if 'suburb' in data['address']:
                address_parts.append(data['address']['suburb'])
            return ', '.join(address_parts) if address_parts else "Adresse inconnue"
        else:
            print(f"Erreur HTTP : {response.status_code}")
            return "Erreur dans la récupération de l'adresse"
    
    except Exception as e:
        if retry < 3:  # Limite de réessai
            print(f"Erreur, nouvelle tentative ({retry + 1})")
            return get_address(latitude, longitude, retry=retry+1)
        else:
            print(f"Erreur lors de la récupération de l'adresse : {e}")
            return "Erreur dans la récupération de l'adresse"




@socketio.on('location_update')
def handle_location_update(data):
    print(f"Localisation reçue : Latitude {data['latitude']}, Longitude {data['longitude']}")

if __name__ == '__main__':
    # Flask écoute sur toutes les interfaces pour être accessible depuis d'autres appareils du réseau local
    socketio.run(app, debug=True)
