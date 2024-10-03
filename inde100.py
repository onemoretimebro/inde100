import streamlit as st

# URL de ton serveur où envoyer l'image
server_url = "http://192.168.1.3:5000/upload"

# JavaScript pour capturer l'image de la caméra toutes les 3 secondes et l'envoyer au serveur
camera_access_script = f"""
<script>
async function startCamera() {{
    // Demander l'accès à la caméra arrière
    const videoStream = await navigator.mediaDevices.getUserMedia({{ 
        video: {{ facingMode: "environment" }}, 
        audio: false 
    }});

    const video = document.querySelector('video');
    video.srcObject = videoStream;

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Capturer une image toutes les 3 secondes et l'envoyer au serveur
    setInterval(() => {{
        // Configurer le canvas pour la capture de l'image
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Dessiner la vidéo sur le canvas (capturer l'image)
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convertir l'image capturée en données base64
        const imageData = canvas.toDataURL('image/jpeg');

        // Envoyer l'image au serveur via une requête POST
        fetch("{server_url}", {{
            method: "POST",
            body: JSON.stringify({{ image: imageData }}),
            headers: {{
                "Content-Type": "application/json"
            }}
        }}).then(response => response.text())
          .then(data => {{
              console.log('Réponse du serveur:', data);
          }})
          .catch((error) => {{
              console.error('Erreur lors de l\'envoi de l\'image:', error);
          }});
    }}, 3000);  // Capture et envoie toutes les 3 secondes
}}

startCamera();
</script>

<video autoplay style="width:100%"></video>
st.write(camera_access_script, unsafe_allow_html=True)
