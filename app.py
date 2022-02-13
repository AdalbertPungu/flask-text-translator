import requests, os, uuid, json
from dotenv import load_dotenv

# Saisir notre clé
load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session

# Créer l'application pour Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Faire l'appel en utilisant post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Récupérer la réponse JSON
    translator_response = translator_request.json()
    # Récupérer la traduction
    translated_text = translator_response[0]['translations'][0]['text']

    # Appelez le modèle de rendu, en passant le texte traduit,
    # texte d'origine et langue cible du modèle
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
    
