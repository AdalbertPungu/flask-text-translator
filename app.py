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

    # Indication de ce que je veux traduire, la version de l'API (3.0) et la langue ciblé
    path = '/translate?api-version=3.0'
    # Ajout des paramètres de la langue ciblé
    target_language_parameter = '&to=' + target_language
    # Création d'un URL complet
    constructed_url = endpoint + path + target_language_parameter

    # Configuration des informations de header, qui incluent notre clé d'abonnement
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Créer le corps de la requête avec le texte à traduire
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
    
